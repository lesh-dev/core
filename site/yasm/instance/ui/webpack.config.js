ExtractTextPlugin = require('extract-text-webpack-plugin');
webpack = require('webpack');
fsm = require('fs');
path = require('path');


const mode = {
    ENV: process.env.NODE_ENV || 'development',
};
const ifdef_query = require('querystring').encode(mode);

let config = {};
try {
    config = require('./config');
} catch (e) {
    config = {
        proxyScheme: 'http',
        proxyHost: 'localhost',
        proxyPort: '8000',
        devServerHost: 'localhost',
        devServerPort: '8080',
    }
}
console.log(config);

const fullProxy = `${config.proxyScheme}://${config.proxyHost}:${config.proxyPort}`;

module.exports = {
    entry: {
        // admin: './src/js/pages/admin.tsx',
        components: './src/js/pages/react-components.tsx',
        internal: './src/js/pages/internal.tsx',
        login: './src/js/pages/login.tsx',
        person_card: './src/scss/cards/person_card/person_card.scss',
        attributes_table: './src/scss/attributes_table.scss'
    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: ['ts-loader', `ifdef-loader?${ifdef_query}`],
                include: [
                    path.resolve(__dirname, 'src'),
                    path.resolve(__dirname, 'node_modules/webpack-dev-server'),
                ],
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
            },
            {
                test: /\.svg/,

                loader: 'babel-loader!react-svg-loader',
            },
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
        filename: '[name].min.js',
    },
    stats: {
        modules: false,
        children: false,
    },
    devtool: "source-map",
    mode: mode.ENV,
    plugins: [
        new ExtractTextPlugin('/../css/pack/[name].css'),
    ],
    devServer: {
        compress: true,
        host: config.devServerHost,
        port: config.devServerPort,
        headers: {
            'X-Forward-Host': `${config.devServerHost}:${config.devServerPort}`,
        },
        before: function (app, server) {
            app.get('/static/**', function (req, res) {
                console.log(`requested ${req.path} from WDS`);
                const p = req.path.split('/').filter(e => e !== '');
                const entry = p.slice(-1).pop();

                if (p[1] === 'js') {
                    const server_path = __dirname.split('/').filter(e => e !== '');
                    server_path[server_path.length - 1] = 'static';
                    server_path.push('js');

                    let data = server.middleware.fileSystem.data;
                    for (const server_path_part of server_path) {
                        data = data[server_path_part]
                    }

                    res.setHeader('Content-Type', 'application/javascript');
                    res.write(
                        data[entry].toString('utf-8')
                    );
                } else if (p[1] === 'css' && p[2] === 'pack') {
                    res.write(
                        server.middleware.fileSystem.data.css['pack'][entry].toString('utf-8')
                    );
                } else {
                    const type = entry.split('.').filter(e => e !== '').slice(-1).pop();
                    if (type === 'svg') {
                        res.setHeader('Content-Type', 'image/svg+xml');
                    }
                    res.write(
                        fsm.readFileSync(path.join(__dirname, '..', req.path))
                    );
                }
                res.flush();
                res.end();
            });
        },
        proxy: {
            '!/static/**': {
                target: fullProxy,
                secure: false,
                changeOrigin: true,
            },
        },
        overlay: {
            warnings: true,
            errors: true
        },
    },
};
