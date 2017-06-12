/**
 * Created by joaogabriellima on 12/06/17.
 */
$().ready(function() {
  demo.checkFullPageBackgroundImage();

  setTimeout(function() {
    // after 1000 ms we add the class animated to the login/register card
    $('.card').removeClass('card-hidden');
  }, 700)
});
