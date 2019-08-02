/**
 * This is the main entrypoint to your Probot app
 * @param {import('probot').Application} app
 */
module.exports = app => {
  // Your code here
  app.log('Yay, the app was loaded!')

  app.on(['pull_request.opened', 'pull_request.closed', 'pull_request.reopened'], async (context) => {
    context.log("Processing a pull request...")
    context.log("Was merged?:", context.payload.pull_request.merged)

    const query = 'bunny';
    const url = `https://source.unsplash.com/random/?${query}`;

    require('https').get(url, (res) => {
      // this is slightly hacky as they are generating a redirection link
      const bunny_link = res.headers.location;
      context.log('Redirect target:', bunny_link);

      if (context.payload.pull_request.merged & context.payload.action == 'closed') {
        const praise = 'Good job on closing that one! Enjoy your reward:';
      } else if (context.payload.action == 'opened') {
        const praise = 'A new pull request, great! Look here...';
      } else {
        const praise = `Well, dunno what\'s goinng on. Grab a ${query} anyway:`;
      }

      const body = `${praise}\n![${query}](${bunny_link})`
      const issueComment = context.issue({ body: body })

      context.log("Commenting:", issueComment)
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
