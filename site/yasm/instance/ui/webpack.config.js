ExtractTextPlugin = require('extract-text-webpack-plugin');
webpack = require('webpack');

const mode = {
    ENV: process.env.NODE_ENV || 'development',
};
const ifdef_query = require('querystring').encode(mode);

module.exports = {
    entry: {
        // admin: './src/js/pages/admin.tsx',
        components: './src/js/pages/react-components.tsx',
        personal: './src/js/pages/personal.tsx',
        login: './src/scss/login/index.scss',
        person_card: './src/scss/cards/person_card/person_card.scss',
        attributes_table: './src/scss/attributes_table.scss'
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: ['ts-loader', `ifdef-loader?${ifdef_query}`],
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
    mode: mode.ENV,
    plugins: [
        new ExtractTextPlugin('/../css/pack/[name].css'),
    ]
}
;