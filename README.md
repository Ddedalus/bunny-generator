# Bunny generator
A toy project to include cute pictures as a reward for completing Pull Requests.

## Setup
```
npm install
```

## Run the bot locally:
```bash
npm run dev
```
This will lead to a registration page if there is no `.env` file in the root directory of the project. Remove the `.env` file if you'd like the registration wizzard again. This may be a convenient way of obtaining the secrets needed for deployment, however you can't change the private key this way as the app would already be registered...

For quick debugging it may be useful to have a separate app registered thiw way on GitHub and have it's secrets in the .env file which is read by `probot` run script. Then the deployment app uses the same code but secrets from the now.json file, which are fetched from now secrets storage directly.

## Deployment on NOW v2
Note: zeit.co runs serverless functions now which requires setup different than described on the probot page. In particular it doesn't use `probot` command to start the bot. To cather for that a separate entry point is provided at `now.js` which loads the relevant plugin and exposes functions from `index.js`.

You need to register your app first with Github and fill the secrets as described below. Only then try to deploy.

### Authentication secrets
To create a new secret in the `new` CLI, run:  
`now secrets add <name> <value>`  
quoting string values. If the string is multiline, use  
`now secrets add <name> -- "<multiline_string>"`  
instead.
The following secrets are required for the app to work:  
  - `bunny-webhook-secret` - anything you'd like, generate random string and paste it on GitHub
  under `https://github.com/settings/apps/your-app-name`
  - `bunny-app-id` - number that the above webpage gives you
  - `bunny-private-key` - the key downloaded from GitHub as a .pem file. To extract it properly, use
  ```bash
    key=$(cat ~/Downloads/bunny-generator.*.private-key.pem)
    # now secrets rm bunny-private-key
    now secrets add bunny-private-key -- "$key"
  ```
  in bash. I couldn't succeed in PowerShell.
  Note that there is something wrong with the way Windows handles these files as the recommended  
  `openssl rsa -in PATH_TO_PEM_FILE -pubout -outform DER | openssl sha1 -c`  
  doesn't give me the correct answer in PowerShell while working fine (same file) with bash.

### Deployment and logs
```bash
now deploy; now log <paste_domain_alias_here> -a -f
``` 
Make sure you also paste the same domain as 'Webhook URL' on the GitHub app configuration page.

To deploy for production (for example automatically add alias on NOW) use the following:
```bash
now --prod
```

### Other remarks
The code uses two nasty cheats currently:
  - to obtain a random picture from unsplash.com/random without messing around with their API, the header of their automatic redirect is used to fetch the actual redirect target. One should replace that with proper API call in the future.
- It comes out that the engine running serverless functions on NOW has some trouble understanding the idea of a callback, causing the program to terminate right after the GET request. To prevent that an old-fashioned wait function is called below (as if they couldn't just give up performance and write thread-blocking code in javascript in the first place... ;) . Of course this puts a nasty lower bound on the runtime of the whole lambda. Reportedly promisses with `await` are a better option but require more setup to run the request.
- it may be nice to introduce an optional config file that allows the user to specify one or more different queries to rnadomise from as the ammount of random bunnies is not infinite...