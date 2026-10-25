#include "windows_support.hpp"
#include <chrono>
#include <iostream>
#include <thread>
namespace winll {
int application(int argc, wchar_t **argv) {
  MutexGuard guard;
  if (argc < 2) {
    std::cout
        << "Windows LL: hash | metadata | processes "
           "[case-sensitive-name-filter] | pe FILE | artifact FILE KEY | "
           "registry KEY | https URL ALLOWED_HOST KEY | hold MILLISECONDS\n";
    return 0;
  }
  const std::wstring cmd = argv[1];
  if (cmd == L"hash" && argc == 2) {
    if (!verify_hashes())
      throw std::runtime_error("hash verification failed");
    event("hash", "vectors and known collision verified");
  } else if (cmd == L"metadata" && argc >= 2) {
    process_metadata();
    for (int i = 0; i < argc; ++i)
      std::cout << "{\"argument_index\":" << i
                << ",\"value\":" << json_quote(utf8(argv[i])) << "}\n";
  } else if (cmd == L"processes" && (argc == 2 || argc == 3))
    process_inventory(argc == 3 ? argv[2] : L"");
  else if (cmd == L"pe" && argc == 3)
    std::cout << pe_json(inspect_pe(read_file(argv[2], 64 * 1024 * 1024)))
              << '\n';
  else if (cmd == L"artifact" && argc == 4) {
    auto b = read_file(argv[2]);
    event("retrieval", "local bytes=" + std::to_string(b.size()));
    validate_artifact(b, read_file(argv[3], 32));
  } else if (cmd == L"registry" && argc == 3)
    validate_artifact(retrieve_registry(), read_file(argv[2], 32));
  else if (cmd == L"https" && argc == 5)
    validate_artifact(retrieve_https(argv[2], argv[3]), read_file(argv[4], 32));
  else if (cmd == L"hold" && argc == 3) {
    std::size_t end = 0;
    auto n = std::stoul(argv[2], &end);
    if (end != std::wstring(argv[2]).size() || n > 30000)
      throw std::runtime_error("hold requires 0..30000 ms");
    event("mutex", "acquired");
    std::this_thread::sleep_for(std::chrono::milliseconds(n));
  } else
    throw std::runtime_error(
        "invalid command/argument count; run without arguments for help");
  return 0;
}
} // namespace winll
