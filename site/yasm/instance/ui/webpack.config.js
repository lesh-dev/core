ExtractTextPlugin = require('extract-text-webpack-plugin');
webpack = require('webpack');

module.exports = {
    entry: {
        school: './src/js/pages/schools.tsx'

    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/
            },
            {
                test: /\.scss$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: ['css-loader', 'sass-loader']
                })
            },
            {
                test: /\.css$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: ['css-loader']
                })
            }
        ]
    },
    resolve: {
        extensions: [
            '.tsx',
            '.ts',
            '.js',
            '.sass'
        ]
    },
    output: {
        path: __dirname + '/../static/js',
        filename: '[name].min.js'
    },
    devtool: "inline-source-map",
    mode: "development",
    plugins: [
        new ExtractTextPlugin('/../css/pack/[name].css'),
    ]
}
;