# Cookie consent

Cookie consent is a Django app to show consent component for web-cookies.

## Quick start

1. Add "cookie\_consent" in your `settings.py`:
```
    ...
    INSTALLED_APPS = [
        ...,
        "cookie_consent",
        ...,
    ]
    ...
```
2. Include the url config like this:
```
    path("cookie_consent/", include("cookie_consent.urls")),
```
3. Run `python manage.py migrate cookie_consent` to create the models.
4. Include consent template in your web-site templates.
  
  For example, I've included the following near the end of my base template:

  ```
  {% block cookie_consent %}
    <link rel="stylesheet" href="{% static 'cookie_consent/css/index.css' %}">
    {% include 'cookie_consent/includes/consent.html' with consent_text='We use cookies to understand your interactions with this web-site.' %}
    {# the default for `consent_text` is 'We are using cookies to make this website fully functional.' #}
    <script defer src="{% static 'cookie_consent/js/main.js' %}"></script>
  {% endblock %}
  ```

  Don't forget to serve that script and css files! You can find them in distribution, css and js are in both source and compiled forms and are fine (as long as you run `collectstatic` command).

5. Start the development server and visit necessary pages.

## Coming up next

- Automated testing
