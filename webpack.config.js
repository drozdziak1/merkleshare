const HtmlWebpackPlugin = require('html-webpack-plugin');
const HtmlWebpackInlineSourcePlugin = require('html-webpack-inline-source-plugin');

module.exports = {
  entry: './merkleshare/webui/webui.js',
  output: {
    path: `${__dirname}/merkleshare/webui/output`,
    filename: 'webui_bundled.js'
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './merkleshare/webui/index.html',
      inlineSource: '.(js|css)$',
    }),
    new HtmlWebpackInlineSourcePlugin(),
  ],
};
