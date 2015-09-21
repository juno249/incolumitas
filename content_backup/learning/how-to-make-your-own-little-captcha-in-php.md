Title: Another wordpress catpcha implementation
Date: 2013-01-25 22:01
Author: admin
Category: Learning, Programming, Security
Slug: how-to-make-your-own-little-captcha-in-php
Status: published

**Hey dear readership and *dudelmatz :)***

I'm kinda overworked and planned quite a while ago to release my own
little captcha implementation to prevent this massive bulk of spam
comments I receive on a daily base: It's obnoxious to scroll through
this sheer amount of spam comments and delete them. You can't just
masstrash them, because you might miss a legit comment and therefore you
need to check every single one. I assume the spammer embrace this
expected behaviour of a blogger, and therefore exploit it.

So I needed to put a stop to this violation of my spare time and I
created my own captcha. Of course, I first searched for a working and
already existing solution (and I am sure there are many which are better
then what I came up with), but the one I used is basically
[crap](http://wordpress.org/extend/plugins/captcha/). [  
](http://wordpress.org/extend/plugins/captcha/)

Its plugin description states:

> *Captcha plugin allows you to protect your website from spam using
> math logic which can be used for login, registration, reseting
> password, comments forms.*

And yeah as I feared this simple elegant captcha is worthless, because
math logic is a joke to parse and solve by computers (=\>spamscripts). I
was pissed and in a mood to write my first wordpress plugin, so I did my
own from scratch.

Well, I need to warn you: My solution is designed to work only on this
site, because it wouldn't be all too hard to crack it and to bypass its
deception. But this won't happen, because there's no reason: This site
has by far not the critical traffic (not yet) which would make it
interesting for a spammer to circumwent the captcha.

Well enough said, you can see the plugin in action on this site (see the
comments section). Here's the source:

    ID;

        if ($uid != 1) {
            if (!isset($_POST['ccaptcha']))
              wp_die(__('Error: You need to enter the captcha.'));

            $answer = strip_tags($_POST['ccaptcha']);
            $generated = get_option('ccaptcha');

            if (strcasecmp($answer, $generated) != 0)
              wp_die(__('Error: Your supplied captcha is incorrect.'));
        }
        return $commentdata;
    }

    /*
     * Create the captcha and store the string in the database.
     */
    function ccaptcha_comment_form_defaults($default) {
        $answer = implode('', ccaptcha_generate());
        
        // Well, that is ugly, but how else?
        if (!get_option('ccaptcha'))
            add_option('ccaptcha', $answer);
        else
            update_option('ccaptcha', $answer);
        
        if (!is_user_logged_in()) {
            $default['fields']['email'] .= 
                '
                
                '.__('Captcha'). '
                ';
        }
        return $default;
    }

    /*** CunningCaptcha Logic begins ***/

    function ccaptcha_generate() {

      $h = fopen(PPM_FILE, "w");

      if (!$h) {
        echo "fopen() error";
        var_dump(error_get_last());
        exit(1);
      }
      
      $figures = array();
      $str = array();
      for ($index = 0; $index < 7; $index++) {
          $choose = rand(0,3);

          switch ($choose) {
              case 0:
                $figures[$index] = get_1(); $str[$index] = '1';
                break;
              case 1:
                $figures[$index] = get_7(); $str[$index] = '7';
                break;
              case 2:
                $figures[$index] = get_E(); $str[$index] = 'E';
                break;
              case 3:
                $figures[$index] = get_Z(); $str[$index] = 'Z';
                break;
              default:
                break;
          }
      }
      
      $captcha = glue_figures($figures);
      
      $width = FIGURE_SIZE * count($figures);
      $height = count($captcha);
      
      /* write the ppm header */
      if (!fwrite($h, "P3\n$width $height\n255\n")) {
        echo 'fwrite(header) failed';
        exit(1);
      }

      for ($i = 0; $i < $height; $i++) {
        for ($j = 0; $j < $width; $j++) {
             fwrite($h, $captcha[$i][$j]."\t");
        }
        fwrite($h, "\n");
      }

      fclose($h);
      
      /* Convert to png and remove ppm */
      system(sprintf("pnmtopng %s > %s && rm %s;",
                    PPM_FILE, CAPTCHA_PNG, PPM_FILE));
      
      return $str;
    }

    /*
     * Glue the figures together. Expects an array of figures. Returns
     * a single array representing the bitmap, ready to print...
     */
    function glue_figures($array_figures) {
        $captcha = array(array());
        $off = 0;
        
        $pad_size = rand(8,16);
        if ($pad_size % 2 != 0)
            $pad_size -= 1; // make even
        
        $pad_size /= 2;
        $shift = 0;
        
        for ($index = 0; $index < count($array_figures); $index++) {
          $shift = rand(0, $pad_size);
          for ($i = 0; $i < FIGURE_SIZE+$pad_size*2; $i++) {
            for ($j = 0; $j < FIGURE_SIZE; $j++) {
              $off = FIGURE_SIZE * $index + $j;
              $captcha[$i][$off] = rand_grey();
              if ($i > $pad_size && $i < FIGURE_SIZE+$pad_size) {
                $captcha[$i-$shift][$off] = $array_figures[$index][$i-$pad_size][$j];
              }
            }
          }
        }
        return $captcha;
    }

    /* Get a random grey scale color to make some noise :) */
    function rand_grey() {
        $grey = rand(0, 180);
        return sprintf("%s %s %s", $grey, $grey, $grey);
    }

    /* Get a random color */
    function rand_color() {
        return sprintf
        (
                "%s %s %s",
                rand(0, 255),
                rand(0, 255),
                rand(0, 255)
        );
    }

    function get_1() {
      $one = array(array());
      // Apply a random shift
      $r_offset = rand(0, FIGURE_SIZE/2);
      // the number of changing the brush color of the figure
      $n_color_changes = FIGURE_SIZE / 
                (rand(0, NUM_BRUSH_CHANGES_MAX) + 1);
      // Get a random brush
      $brush = rand_color();

      for ($i = 0; $i < FIGURE_SIZE; $i++) {
        if ($i % $n_color_changes == 0)
            $brush = rand_color();
        
        for ($j = 0; $j < FIGURE_SIZE; $j++) {

        // Fill the rest with greyscale colors
        $one[$i][$j] = rand_grey(); 
        
        // The tree of the '1'
        if ($j == FIGURE_SIZE-1-$r_offset || 
            $j == FIGURE_SIZE-2-$r_offset) {
           $one[$i][$j] = $brush;
        }

        // The hook of the '1'
        if (($i + $j == FIGURE_SIZE-1-$r_offset && $i < (FIGURE_SIZE-1)/2) ||
            ($i+1 + $j == FIGURE_SIZE-1-$r_offset && $i < (FIGURE_SIZE-1)/2))
            $one[$i][$j] = $brush;
        }
      }
      return $one;
    }

    function get_7() {
      $seven = array(array());
      // Apply a random shift
      $r_offset = rand(0, FIGURE_SIZE/2);
      // the number of changing the brush color of the figure
      $n_color_changes = FIGURE_SIZE / 
                (rand(0, NUM_BRUSH_CHANGES_MAX) + 1);
      // Get a random brush
      $brush = rand_color();
      
      for ($i = 0; $i < FIGURE_SIZE; $i++) {
        if ($i % $n_color_changes == 0)
            $brush = rand_color();
        
        for ($j = 0; $j < FIGURE_SIZE; $j++) {
            
          // Fill the rest with greyscale colors
          $seven[$i][$j] = rand_grey();
          
          // The roof of the '7'
          if (($i == 0 || $i == 1) &&
                  $j > (FIGURE_SIZE-1)/2)
            $seven[$i][$j-$r_offset] = $brush;
          
          // The tree of the '7'
          if (  ($i/2 + $j) == FIGURE_SIZE-1-$r_offset      ||
                ($i/2 + $j-1) == FIGURE_SIZE-1-$r_offset    ||
                (($i+1)/2 + $j) == FIGURE_SIZE-1-$r_offset  ||
                (($i+1)/2 + $j-1) == FIGURE_SIZE-1-$r_offset )
            $seven[$i][$j] = $brush;
        }
      }
      return $seven;
    }

    function get_Z() {
      $z = array(array());
      // Apply a random shift
      $r_offset = rand(0, FIGURE_SIZE/2);
      // the number of changing the brush color of the figure
      $n_color_changes = FIGURE_SIZE / 
                (rand(0, NUM_BRUSH_CHANGES_MAX) + 1);
      // Get a random brush
      $brush = rand_color();
      
      for ($i = 0; $i < FIGURE_SIZE; $i++) {
        if ($i % $n_color_changes == 0)
            $brush = rand_color();
        
        for ($j = 0; $j < FIGURE_SIZE; $j++) {
            
          // Fill the rest with greyscale colors
          $z[$i][$j] = rand_grey();
          
          // The roof and soil of the 'Z'
          if ((($i == 0 || $i == 1) || 
              ($i == FIGURE_SIZE-1 || $i == FIGURE_SIZE-2)) &&
               $j > (FIGURE_SIZE-1)/2)
            $z[$i][$j-$r_offset] = $brush;
          
          // The tree of the 'Z'
          if (  ($i/2 + $j) == FIGURE_SIZE-1-$r_offset      ||
                ($i/2 + $j-1) == FIGURE_SIZE-1-$r_offset    ||
                (($i+1)/2 + $j) == FIGURE_SIZE-1-$r_offset  ||
                (($i+1)/2 + $j-1) == FIGURE_SIZE-1-$r_offset )
            $z[$i][$j] = $brush;
        }
      }
      return $z; 
    }

    function get_E() {  
      $e = array(array());
      // Apply a random shift
      $r_offset = rand(0, FIGURE_SIZE/2);
      // the number of changing the brush color of the figure
      $n_color_changes = FIGURE_SIZE / 
                (rand(0, NUM_BRUSH_CHANGES_MAX) + 1);
      // Get a random brush
      $brush = rand_color();
      
      for ($i = 0; $i < FIGURE_SIZE; $i++) {
        if ($i % $n_color_changes == 0)
            $brush = rand_color();
        
        for ($j = 0; $j < FIGURE_SIZE; $j++) {     
            
          // Fill the rest with greyscale colors
          $e[$i][$j] = rand_grey();
          
          // The left vertical bar
          if ($j == FIGURE_SIZE/2-$r_offset ||
              $j == FIGURE_SIZE/2-1-$r_offset)
            $e[$i][$j] = $brush;
          
          // The three balks of the 'E'
          if ((($i == 0 || $i == 1) || 
              ($i == FIGURE_SIZE-1 || $i == FIGURE_SIZE-2) ||
              ($i == FIGURE_SIZE/2-1 || $i == FIGURE_SIZE/2-2))
              /* prevent out of bounds indices */
              && $j > (FIGURE_SIZE-1)/2)
            $e[$i][$j-$r_offset] = $brush;
        }
      }
      return $e;
    }
    ?>
