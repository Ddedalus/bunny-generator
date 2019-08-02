/**
 * This is the main entrypoint to your Probot app
 * @param {import('probot').Application} app
 */
module.exports = app => {
  // Your code here
  app.log('Yay, the app was loaded!')

  app.on(['pull_request.opened', 'pull_request.closed', 'pull_request.reopened'], async (context) => {
    context.log(context)
    context.log("Processing an issue...")
    context.log("Was merged?:", context.payload.pull_request.merged)
    const query = 'bunny';
    const url = `https://source.unsplash.com/random/?${query}`;
    // const context = context;
    var https = require('https');
    https.get(url, (res) => {
      context.log('Redirect:', res.headers.location);

      const bunny_link = res.headers.location || url;
      const body = `Good job! Enjoy:\n\
        ![Cute bunny](${bunny_link})`
      const issueComment = context.issue({ body: body })

      context.log("Publishing an issue:", issueComment)
      context.github.issues.createComment(issueComment)

    });
    function wait() {
      return new Promise((resolve, reject) => {
        setTimeout(() => resolve("hello"), 1000)
      });
    }
    await wait();
  })

  // For more information on building apps:
  // https://probot.github.io/docs/

  // To get your app running against GitHub, see:
  // https://probot.github.io/docs/development/
}
