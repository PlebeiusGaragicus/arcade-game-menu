tips = """
https://pywebio.readthedocs.io/en/latest/cookbook.html

https://github.com/pywebio/PyWebIO

https://pywebio.readthedocs.io/en/latest/guide.html
https://pywebio.readthedocs.io/en/latest/guide.html?highlight=example#layout

https://pywebio.readthedocs.io/en/latest/battery.html


"""

import time
import logging
logger = logging.getLogger()
import hashlib

import pywebio

BUTTON_RESTART = "Kill menu system"
BUTTON_KILL = "Kill currently running app"


from lnarcade.app import App

class ArcadeServerPage():
    def __init__(self, env_filepath: str):
        self.password = "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb" #a
        self.env_filepath = env_filepath

    def start_server(self):
        pywebio.start_server(applications=self.check_password,
                             host="0.0.0.0",
                             port=8080,
                             auto_open_webbrowser=False,
                        )

    def restart(self):
        logger.warning("Killing the menu system!")
        App.get_instance().kill_running_process() # make sure any app doesn't keep running
        App.get_instance().window.close()
        exit(0)

    def kill_app(self):
        if App.get_instance().process is None:
            logger.warning("No process to kill")
            pywebio.output.toast("No process to kill", duration=7, color="warn")
            return

        logger.warning("Killing the current process!")
        App.get_instance().kill_running_process()


    def load_env(self):
        with open(self.env_filepath, "r") as f:
            lines = f.read()

            return lines


    def save_env(self, env):
        with open(self.env_filepath, "w") as f:
            f.writelines(env)
        
        pywebio.output.toast("Saved!", duration=7, color="success")


    def backend_page(self):
        pywebio.output.put_markdown("# Lightning Arcade Settings Backend")
        pywebio.output.put_markdown("---")

        # Command buttons
        pywebio.output.put_button(BUTTON_RESTART, onclick=self.restart, color="danger")
        pywebio.output.put_button(BUTTON_KILL, onclick=self.kill_app, color="warning")

        # config file editor
        pywebio.output.put_markdown("---")
        pywebio.output.put_markdown("## .env file editor")
        env_contents = self.load_env()
        pywebio.pin.put_textarea("env", value=self.load_env(), rows=env_contents.count("\n")+1, placeholder="Error loading env file")
        pywebio.output.put_button("Save", onclick=lambda: self.save_env(pywebio.pin.pin["env"]), color="success")

        pywebio.output.put_markdown("---")
        pywebio.output.put_markdown(tips)


    def check_password(self):
        pywebio.output.toast("Unauthorized access - close this webpage!", duration=5, color="error")
        # time.sleep(5) # TODO: uncomment in production

        access = False

        while not access:
            # pywebio.session.hold() # TODO - Use pins for this part?  Hmm..
            user_input = pywebio.input.input("Enter password", type=pywebio.input.PASSWORD)

            attempt_hash = hashlib.sha256(user_input.encode()).hexdigest()

            if attempt_hash != self.password:
                # TODO - can I find a way to slow this down so it can't be brute forced?
                pywebio.output.toast("Incorrect password", duration=7, color="error")
                time.sleep(10)
            else:
                access = True

        self.backend_page()
        pywebio.session.hold()


if __name__ == "__main__":
    server = ArcadeServerPage( "/Users/myca/.config/.lnarcade" )
    server.start_server()




GPTadvice = """
Certainly! Security is of utmost importance, especially when dealing with configuration settings. Here are a few security measures you can implement for your PyWebIO application:

1. **Use HTTPS**: Ensure your PyWebIO server is running over HTTPS to encrypt the data in transit. This will prevent eavesdropping of sensitive data like passwords. You can set up HTTPS with libraries like Flask and then serve PyWebIO over Flask, using a library like `Flask-Talisman` for HTTPS. For a production environment, consider using a reverse proxy setup with something like Nginx, and let it handle HTTPS with certificates from Let's Encrypt.

2. **Stronger Password Mechanism**:
    - Use a stronger password.
    - Use hashing to compare passwords. Store a hashed version of your password and then compare user input against the hashed version. This ensures the password is never stored in plain text.
    - Add a rate limiting mechanism. This will slow down repeated login attempts, which helps prevent brute-force attacks.

3. **CORS Headers**: If you're making requests across domains, ensure you have the correct CORS headers set up to prevent cross-site request forgery.

4. **Input Validation**: Always validate and sanitize inputs to prevent SQL injection, script injection, and other injection attacks. Even if you're not directly interfacing with a database here, ensuring your inputs are sanitized and expected can prevent potential vulnerabilities.

5. **Environment Isolation**: Only expose the necessary environment variables in `.env` to this application. This way, even if someone gets access, they won't be able to see/change critical environment variables.

6. **Session Management**: Add proper session management. Once a user logs in, provide them with a session token (JWT or similar) and check the validity of this token for all subsequent requests.

7. **Logging**: Log all access attempts (both successful and unsuccessful). This way, you can monitor for any suspicious activities.

8. **Update Libraries Regularly**: Regularly update all your dependencies to their latest versions to ensure you have the most recent security patches.

Here's a basic way to implement some of the password-related enhancements:

```python
import hashlib

class ArcadeServerPage():
    def __init__(self):
        self.password_hash = self.hash_password("Your_Strong_Password")

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self):
        password = pywebio.input.input("Enter password", type=pywebio.input.PASSWORD)
        if self.hash_password(password) != self.password_hash:
            # Rate limit here
            time.sleep(5)
            return
        self.backend_page()
```

Note: This is a simple hashing mechanism, and in a real-world scenario, you might want to add salt to the password before hashing to make it even more secure.

For additional security measures, consider moving sensitive operations and configurations out of the web environment entirely. Allow only necessary actions through the web interface.
"""