import { Application } from 'probot' // eslint-disable-line no-unused-vars

export = (app: Application) => {
  app.on(['issues.opened', 'issues.closed'], async (context) => {

    const body = 'Good job! Enjoy:\n\
    ![Cute bunny](https://www.bing.com/th?id=OIP.EGnMzdVyePJWuvk6dZOJqgHaEo&pid=Api&rs=1)'
    const issueComment = context.issue({ body: body})
    await context.github.issues.createComment(issueComment)
  })
  // For more information on building apps:
  // https://probot.github.io/docs/

  // To get your app running against GitHub, see:
  // https://probot.github.io/docs/development/
}
