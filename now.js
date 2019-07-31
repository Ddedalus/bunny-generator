var { serverless } = require('@chadfawcett/probot-serverless-now')
const appFn = require('./public/')
module.exports = serverless(appFn)