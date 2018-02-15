<?php
include('/var/www/html/templates/head.php');
include('/var/www/html/lib/{{ phplib }}.php');

/* This template was generated using formit and jinja2
 * at {{ gentime }}, on {{ blah }}
 */
?>

  <link href="<?php base_url(); ?>/css/bootstrap-datetimepicker.css"

<div class="container">

  <h2> {{ appname }} </h2><hr/>
  <h4 class="pull-right"><a href="<?php print($base_url); ?>/documentation/geode.php" target="_blank">Need help? <span class="glyphicon glyphicon-question-sign" aria-hidden="true"></span></a></h4>

  <!-- div for incoming alerts to be attached -->
  <div class="row" id="alerts"></div>

  <!-- input array div -->
  <div class="row">
    <form id="form" action"<?php echo(base_url() . "/applications/{{ appname }}"); ?>" method="POST">
    {% for param in params %}
      { param.tohtml() }
    {% endfor %}
    </form>
  </div>

  <!-- results array div -->
  <div class="row-fluid">
    {% for input in inputs %}
      { result.tohtml() }
    {% endfor %}
  </div>

</div>

<!-- javascript settings -->
<script type="text/javascript">
{{ jssettings }}
</script>

<!-- main javascript source for this app -->
<script type="text/javascript" src="<?php base_url(); ?>/js/lib/{{ appname }}.js"></script>

<?php include("/var/www/html/templates/footer.php"); ?>

