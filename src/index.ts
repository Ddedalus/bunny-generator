import { Application } from 'probot' // eslint-disable-line no-unused-vars
import { get } from 'https'


export = (app: Application) => {
  console.log('The app has just started!');
  app.on(['issues.opened', 'issues.closed', 'issues.reopened'], async (context) => {
    
    const query = 'bunny';
    const url = `https://source.unsplash.com/random/?${query}`;
    await get(url, (res) => {
      console.log('Redirect:', res.headers.location);
      
      const bunny_link: string = res.headers.location || url;
      const body = `Good job! Enjoy:\n\
      ![Cute bunny](${bunny_link})`
      console.log("Publishing an issue:", body)
      
      const issueComment = context.issue({ body: body})
      context.github.issues.createComment(issueComment)

    }).on('error', (e) => {
      console.error(e);
    });
  })
  // For more information on building apps:
  // https://probot.github.io/docs/

  // To get your app running against GitHub, see:
  // https://probot.github.io/docs/development/
}
