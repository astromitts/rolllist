# Rollist

Rollist is a productivity application built using Django, JQuery and SASS.

The template is based on (shockingly) Bootstrap.

It is hosted on Heroku.

You can read more about it's user interface and [see it live here](https://www.rollist.app/) (and even use it if you want)!

## Design Principals

This app uses a combination of SASS and JQuery to achieve its user experience. In the HTML, I have attempted something close to a BEM model when it comes to naming and nesting elements on the page. Any element that is required for JQuery functionality should have a class named like 'js-something-something', and this class should NOT be a styled SASS element. This helps to ensure that I can change the visual of a page without breaking the functionality, and vice-versa.

The Django code is mostly covered in test cases, which also serves to document intended usage -- though of course there is room for improvement and ample doc strings and code comments to help with this as well. 