#include "windows_support.hpp"
#include <algorithm>
#include <bcrypt.h>
namespace winll {
namespace {
void check(NTSTATUS s, const char *label) {
  if (s < 0)
    throw std::runtime_error(std::string(label) + ": CNG status " +
                             std::to_string(static_cast<long>(s)));
}
struct Secret {
  Bytes b;
  explicit Secret(Bytes v) : b(std::move(v)) {}
  ~Secret() {
    if (!b.empty())
      SecureZeroMemory(b.data(), b.size());
  }
};
struct Algorithm {
  BCRYPT_ALG_HANDLE h = nullptr;
  ~Algorithm() {
    if (h)
      BCryptCloseAlgorithmProvider(h, 0);
  }
};
struct Key {
  BCRYPT_KEY_HANDLE h = nullptr;
  ~Key() {
    if (h)
      BCryptDestroyKey(h);
  }
};
} // namespace
void validate_artifact(const Bytes &b, Bytes keybytes) {
  Secret key(std::move(keybytes));
  if (key.b.size() != 32 || b.size() < 33 || b.size() > 1024 * 1024 ||
      !std::equal(b.begin(), b.begin() + 4, "WLL1"))
    throw std::runtime_error("invalid key/envelope");
  Algorithm alg;
  check(BCryptOpenAlgorithmProvider(&alg.h, BCRYPT_AES_ALGORITHM, nullptr, 0),
        "AES provider");
  check(BCryptSetProperty(alg.h, BCRYPT_CHAINING_MODE,
                          reinterpret_cast<PUCHAR>(
                              const_cast<wchar_t *>(BCRYPT_CHAIN_MODE_GCM)),
                          sizeof BCRYPT_CHAIN_MODE_GCM, 0),
        "GCM mode");
  DWORD n = 0, got = 0;
  check(BCryptGetProperty(alg.h, BCRYPT_OBJECT_LENGTH,
                          reinterpret_cast<PUCHAR>(&n), sizeof n, &got, 0),
        "key object length");
  Secret object{Bytes(n)};
  Key handle;
  check(BCryptGenerateSymmetricKey(alg.h, &handle.h, object.b.data(), n,
                                   key.b.data(),
                                   static_cast<ULONG>(key.b.size()), 0),
        "generate key");
  BCRYPT_AUTHENTICATED_CIPHER_MODE_INFO info;
  BCRYPT_INIT_AUTH_MODE_INFO(info);
  info.pbNonce = const_cast<PUCHAR>(b.data() + 4);
  info.cbNonce = 12;
  info.pbTag = const_cast<PUCHAR>(b.data() + 16);
  info.cbTag = 16;
  info.pbAuthData = const_cast<PUCHAR>(b.data());
  info.cbAuthData = 4;
  Secret plain{Bytes(b.size() - 32)};
  ULONG written = 0;
  check(BCryptDecrypt(handle.h, const_cast<PUCHAR>(b.data() + 32),
                      static_cast<ULONG>(b.size() - 32), &info, nullptr, 0,
                      plain.b.data(), static_cast<ULONG>(plain.b.size()),
                      &written, 0),
        "authenticated decryption");
  plain.b.resize(written);
  if (!valid_schema(plain.b))
    throw std::runtime_error("authenticated data has invalid inert schema");
  event("artifact_validated",
        "authenticated inert schema; plaintext not exported");
}
} // namespace winll
