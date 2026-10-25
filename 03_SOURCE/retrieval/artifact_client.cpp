#include "windows_support.hpp"
#include <chrono>
#include <cwctype>
#include <winhttp.h>
namespace winll {
namespace {
constexpr DWORD limit = 1024 * 1024;
struct Internet {
  HINTERNET h;
  explicit Internet(HINTERNET v) : h(v) {
    wincheck(h != nullptr, "WinHTTP handle");
  }
  ~Internet() { WinHttpCloseHandle(h); }
  Internet(const Internet &) = delete;
  Internet &operator=(const Internet &) = delete;
};
struct Registry {
  HKEY h = nullptr;
  ~Registry() {
    if (h)
      RegCloseKey(h);
  }
};
} // namespace
Bytes retrieve_registry() {
  Registry k;
  auto s =
      RegOpenKeyExW(HKEY_CURRENT_USER, L"Software\\WindowsLL\\TestArtifacts", 0,
                    KEY_QUERY_VALUE, &k.h);
  if (s != ERROR_SUCCESS)
    throw std::runtime_error("test registry key unavailable: " +
                             std::to_string(s));
  DWORD n = 0;
  s = RegGetValueW(k.h, nullptr, L"Data", RRF_RT_REG_BINARY, nullptr, nullptr,
                   &n);
  if (s != ERROR_SUCCESS || n > limit)
    throw std::runtime_error("invalid registry artifact size/type");
  Bytes b(n);
  DWORD actual = n;
  s = RegGetValueW(k.h, nullptr, L"Data", RRF_RT_REG_BINARY, nullptr, b.data(),
                   &actual);
  if (s != ERROR_SUCCESS || actual > n)
    throw std::runtime_error("registry read changed or failed");
  b.resize(actual);
  event("retrieval", "registry bytes=" + std::to_string(b.size()));
  return b;
}
Bytes retrieve_https(const std::wstring &url, const std::wstring &allowed) {
  if (allowed.empty() ||
      allowed.find_first_not_of(L"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRS"
                                L"TUVWXYZ0123456789.-") != std::wstring::npos)
    throw std::runtime_error("explicit DNS host allowlist required");
  URL_COMPONENTS c{};
  c.dwStructSize = sizeof c;
  c.dwHostNameLength = c.dwUrlPathLength = c.dwExtraInfoLength =
      c.dwUserNameLength = c.dwPasswordLength = static_cast<DWORD>(-1);
  wincheck(WinHttpCrackUrl(url.c_str(), static_cast<DWORD>(url.size()), 0, &c),
           "WinHttpCrackUrl");
  std::wstring host(c.lpszHostName, c.dwHostNameLength);
  if (c.nScheme != INTERNET_SCHEME_HTTPS || c.nPort != 443 ||
      c.dwUserNameLength || c.dwPasswordLength ||
      _wcsicmp(host.c_str(), allowed.c_str()) != 0)
    throw std::runtime_error("HTTPS source rejected by allowlist");
  std::wstring path(c.lpszUrlPath, c.dwUrlPathLength);
  if (path.empty())
    path = L"/";
  if (c.dwExtraInfoLength)
    path.append(c.lpszExtraInfo, c.dwExtraInfoLength);
  if (path.find(L'#') != std::wstring::npos)
    throw std::runtime_error("URL fragments forbidden");
  Internet session(
      WinHttpOpen(L"WindowsLL-Research/1", WINHTTP_ACCESS_TYPE_NO_PROXY,
                  WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0));
  wincheck(WinHttpSetTimeouts(session.h, 5000, 5000, 5000, 5000), "timeouts");
  Internet connection(WinHttpConnect(session.h, host.c_str(), 443, 0));
  Internet request(WinHttpOpenRequest(
      connection.h, L"GET", path.c_str(), nullptr, WINHTTP_NO_REFERER,
      WINHTTP_DEFAULT_ACCEPT_TYPES, WINHTTP_FLAG_SECURE));
  DWORD policy = WINHTTP_OPTION_REDIRECT_POLICY_NEVER;
  wincheck(WinHttpSetOption(request.h, WINHTTP_OPTION_REDIRECT_POLICY, &policy,
                            sizeof policy),
           "redirect policy");
  wincheck(WinHttpSendRequest(request.h, WINHTTP_NO_ADDITIONAL_HEADERS, 0,
                              WINHTTP_NO_REQUEST_DATA, 0, 0, 0),
           "HTTPS send");
  wincheck(WinHttpReceiveResponse(request.h, nullptr), "HTTPS receive");
  DWORD status = 0, size = sizeof status;
  wincheck(WinHttpQueryHeaders(
               request.h, WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER,
               WINHTTP_HEADER_NAME_BY_INDEX, &status, &size,
               WINHTTP_NO_HEADER_INDEX),
           "HTTPS status");
  if (status != 200)
    throw std::runtime_error("HTTPS status " + std::to_string(status));
  Bytes b;
  const auto deadline =
      std::chrono::steady_clock::now() + std::chrono::seconds(30);
  unsigned char chunk[4096];
  DWORD got = 0;
  do {
    if (std::chrono::steady_clock::now() > deadline)
      throw std::runtime_error("HTTPS overall read deadline exceeded");
    wincheck(WinHttpReadData(request.h, chunk, sizeof chunk, &got),
             "HTTPS read");
    if (got > limit - b.size())
      throw std::runtime_error("HTTPS artifact exceeds size cap");
    b.insert(b.end(), chunk, chunk + got);
  } while (got);
  event("retrieval", "HTTPS bytes=" + std::to_string(b.size()));
  return b;
}
} // namespace winll
