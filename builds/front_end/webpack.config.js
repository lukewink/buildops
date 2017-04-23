var HtmlWebpackPlugin = require('html-webpack-plugin')
var BundleTracker = require('webpack-bundle-tracker')
var path = require('path')

var HtmlWebpackPluginConfig = new HtmlWebpackPlugin({
    template: __dirname + '/app/index.html',
    inject: 'body'
})

module.exports = {
    entry: [
        './app/index.js'
    ],
    output: {
        path: path.resolve('../static/bundles'),
        filename: "index_bundle.js"
    },
    module: {
        rules: [
            {test: /\.js$/, exclude: /node_modules/, loader: "babel-loader"}
        ]
    },
    plugins: [
        HtmlWebpackPluginConfig,

        // Tells webpack where to store data about the bundle
        new BundleTracker({filename: './webpack-stats.json'})
    ],
}