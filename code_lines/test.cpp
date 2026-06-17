#include <Windows.h>
#include <iostream>

std::string str = R"(
这是一个原始字符串字面量，包含特殊字符，如换行符和引号，不需要转义
/* 这是一个多行注释 */
// 这是一个单行注释
/**
 * 这是一个文档注释
 * 可以用于生成文档
 */
)";

//    这是一个C++程序

/**
 * 这是一个多行注释
 * 这是一个多行注释
 */
int c = 1;

/**
 * *这是一个多行注释*
 * /**
 * * 这是一个多行注释*
 */

/*This is a single-line comment*/ int a = 1;

template <typename T>
class MyClass
{
public:
    MyClass() = default; // 默认构造函数
    MyClass(const MyClass &) = default;
    MyClass &operator=(const MyClass &) = default;
    MyClass(MyClass &&) = default;
    MyClass &operator=(MyClass &&) noexcept = default;
    ~MyClass() = default;
};

class Test
{
public:
    Test() = default;
    Test(const Test &) = default;
    Test &operator=(const Test &) = default;
    Test(Test &&) = default;
    Test &operator=(Test &&) noexcept = default;
    ~Test() = default;

private:
    int x = 0;
};

int *p{nullptr};
Test t{};
MyClass<int> myClass{};

int main(int argc, char *argv[])
{
    std::cout << "Hello, World !" << std::endl;
    std::cout << "            //Hello, World !" << std::endl;
    std::cout << "/*    Hello, World !      */" << std::endl;

    TEXT("Hello, World !");

    return 0;
}