<?php
include('{{ phplibpath }}.php');
include('{{ frontroot }}/head.php');

/* This form was generated using formit and jinja2
 * on{{ gentime }}
 */
?>

{% for dep in cssdependencies %}
    { dep }
{% endfor %}

{% for dep in jsdependencies %}
    { dep }
{% endfor %}

<div class="container">

  <h2> {{ appname }} </h2><hr/>

  <h4 class="pull-right"><a href="<?php print($base_url); ?>/documentation/{{ appslug }}.php" target="_blank">Need help? <span class="glyphicon glyphicon-question-sign" aria-hidden="true"></span></a></h4>

  <!-- div for incoming alerts to be attached -->
  <div class="row" id="alerts"></div>

  <!-- input array div -->
  <div class="row">
    <form id="form" action"<?php echo(base_url() . "/applications/{{ appslug }}"); ?>" method="POST">

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
<script type="text/javascript" src="/{{ appslug }}.js"></script>

<?php include('{{ frontroot }}/footer.php'); ?>

