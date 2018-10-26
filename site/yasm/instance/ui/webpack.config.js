ExtractTextPlugin = require('extract-text-webpack-plugin');
webpack = require('webpack');

module.exports = {
    entry: {
        admin: './src/js/pages/admin.tsx',
        components: './src/js/pages/react-components.tsx',
        personal: './src/js/pages/personal.tsx',
        login: './src/scss/login/index.scss'
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
    stats: {
        modules: false,
        children: false,
    },
    devtool: "source-map",
    mode: "development",
    plugins: [
        new ExtractTextPlugin('/../css/pack/[name].css'),
    ]
}
;