#include <protobuf-c.h>

int main() {
    // this will crash. But we just need to make sure it compiles and links
    protobuf_c_enum_descriptor_get_value_by_name(NULL, "abcd");
}
