## Website Code ##

[philiplessner.com](http://www.philiplessner.com)

### Website Organization ###

|Blueprint|Route|Database|Database Table|
|---------|-----|--------|--------------|
|public|/|_ |_ |
|public|/blog<br>&emsp;/blog/xxx<br>.<br>.<br>.<br>&emsp;/blog/yyy|website.db|blogs_table|
|public|/aboutme/|website.db|references_table|
|public|/photos/xxx<br>.<br>.<br>.<br>/photos/yyy|website.db|images_table<br>pages_table|
|admin|/login|website.db|users_table|
|admin|/signup|website.db|users_table|
|admin|/blogselect|website.db|blogs_table|
|admin|/blogedit/xxx|website.db|blogs_table|
|admin|/analytics|logs.db|logs_table|
        

### Frontend assets

Install and build the CodeMirror editor bundle with:

```sh
npm install
npm run build
```

Run `npm run build:watch` while editing files in `frontend/`.
