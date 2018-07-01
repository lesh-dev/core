module.exports = {
    entry: {
        school: './src/js/school.tsx'

    },
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/
            }
        ]
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js']
    },
    output: {
        path: __dirname + '/../static/js',
        filename: '[name].min.js'
    }
};