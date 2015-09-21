Title: Solution for Natas11 for natas wargame on overthewire.org
Date: 2015-09-10 15:57
Author: admin
Category: PHP, Programming, Security, Wargames
Slug: solution-for-natas11-for-natas-wargame-on-overthewire-org
Status: published

Solution for Natas web security wargame with by XORing the plaintext with the ciphertext...
-------------------------------------------------------------------------------------------

Currently I am playing some wargames on
[overthewire.org](http://overthewire.org/wargames/).

The first 10 levels were very easy and everyone with some technical
knowledge and programming experience should be able to solve them. But
somehow I got stuck for a few hours on level 11. The task is to modify a
XOR encrypted cookie. For some reason I couldn't figure out how to
obtain the xor key that was used.

The challenge was to reverse engineer the key by having the plaintext
and the ciphertext. Of course I should have realized very quickly that
xoring the plaintext with the ciphertext yields us back the key. But why
is this so? Consider the following math:  

`plaintext xor ciphertext == key <=> plaintext xor (plaintext xor key) <=> plaintext xor plaintext xor key <=> 00000... xor key == key`

As you can see, the plaintext cancels out. If the plaintext would be a
single byte, say, 1100 1101, then XORing this byte with itself yields:  
`1100 1101 XOR 1100 1101 -------- 0000 0000`

To finally get to solution of the wargame, you can safe the following
file as a PHP file and run it:

    "no", "bgcolor"=>"#ffffff")));
    // the above function outputs
    // qw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jq
    // 7177384a7177384a7177384a7177384a7177384a7177384a7177384a7177384a7177384a7177384a71
    // we can easily see that the xor key must be 'qw8J'

    $key = 'qw8J';
    // generate the new data with the key
    echo 'Submit the following as the "data" cookie to gain access: '.encodeData(array("showpassword"=>"yes", "bgcolor"=>"#ffffff"), $key)."\n";

    ?>

Here a screenshot of the message you get when submitting the generated
cookie:

[![Screenshot - 10.09.2015 -
16:32:49](http://incolumitas.com/wp-content/uploads/2015/09/Screenshot-10.09.2015-163249-1024x484.png)](http://incolumitas.com/wp-content/uploads/2015/09/Screenshot-10.09.2015-163249.png)
