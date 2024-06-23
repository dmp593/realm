const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');


const HTML = {
    // mapping of HTML to generate
    // structure <filename>: <template> (aka <output>: <input>)

    /******* PROJECT ROOT TEMPLATES DIR *******/
    '../templates/components/header.html': 'src/templates/components/header.html',
    '../templates/components/footer.html': 'src/templates/components/footer.html',
    
    '../templates/base.html': 'src/templates/base.html',
    '../templates/home.html': 'src/templates/home.html',
    '../templates/contacts.html': 'src/templates/contacts.html',

    /******* HOUSES APP TEMPLATES DIR *******/

    // House List
    '../houses/templates/houses/components/form_house_list_filters.html': 'src/templates/houses/components/form_house_list_filters.html',
    '../houses/templates/houses/house_list.html': 'src/templates/houses/house_list.html',

    // House Detail
    '../houses/templates/houses/components/house_card_header.html': 'src/templates/houses/components/house_card_header.html',
    '../houses/templates/houses/components/house_card_summary.html': 'src/templates/houses/components/house_card_summary.html',
    '../houses/templates/houses/house_detail.html': 'src/templates/houses/house_detail.html',
}

const JS = {
    index: {
        src: './src/js/index.js',
        out: 'js/index.js'
    },
    house_list_filters: {
        src: './src/js/houses/house_list_filters.js',
        out: 'js/houses/house_list_filters.js'
    },
    house_detail: {
        src: './src/js/houses/house_detail.js',
        out: 'js/houses/house_detail.js'
    }
}

module.exports = {
    mode: 'production',
    entry: Object.fromEntries(
        new Map(
            Object.keys(JS).map(k => [k, JS[k].src])
        ).entries()
    ),
    output: {
        filename: (pathData) => {
            console.log(JS[pathData.chunk.name].out)
            return JS[pathData.chunk.name].out
        },
        path: path.resolve(__dirname, '../static'),
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: 'css/[name].css',
        }),
        ...Object.keys(HTML).map(k => new HtmlWebpackPlugin({ 
            filename: k,
            template: HTML[k],
            inject: false,
            minify: false,
        }))
    ],
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader']
            }
        ]
    },
};
