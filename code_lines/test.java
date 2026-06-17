import java.util.*;

//  kjsgslkkgj

/**
 * fjslkfksgskljg
 * skjgkjskklk1klj
 */

/**
 * lsjaj111jkwlkjt
 * //jtkejrkjyekjyey
 * /*jsjkgkjlsfkljjkl
 */

/* lsjkfkj14115j2lj53jh46 */

class Class {
    public void func() {
        String str = """
                {
                    // 我不是注释
                    /*我不是注释*/ int x = 1;

                    /**
                     * 我不是注释
                     * //我不是注释
                     * /*我不是注释*/ int c = 1;
                    */

                    /**
                     * 我不是注释
                     * 我不是注释
                    */ int y = 1;
                }
                """;
    }
}

class Derived extends Class {
    @Override
    public void func() {
        String a = """
                tskjflsdjg
                """;
    }
}

public class test {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        int x = s.nextInt();

        System.out.println("Hello, World !");
        s.close();
    }
}