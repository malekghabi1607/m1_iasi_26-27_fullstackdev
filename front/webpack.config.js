const path = require("path");
const webpack = require("webpack");

module.exports = function (env, argv) {
    const build_mode = argv.mode || "production"
    const is_dev_build_mode = build_mode === "development"

    return {
        entry: {
            app: "./src/index.js",
        },
        mode: "development",
        module: {
            rules: [
                {
                    test: /\.(woff2?|eot|ttf|otf)$/i,
                    type: "asset/resource",
                },
                {
                    test: /\.(js|jsx)$/,
                    exclude: /(node_modules|bower_components)/,
                    loader: "babel-loader",
                    options: { presets: ["@babel/env", "@babel/react"] },
                },
                {
                    test: /\.css$/,
                    use: ["style-loader", "css-loader"],
                },
                {
                    test: /\.s[ac]ss$/i,
                    use: [
                        // Creates `style` nodes from JS strings
                        "style-loader",
                        // Translates CSS into CommonJS
                        "css-loader",
                        // Compiles Sass to CSS
                        {
                            loader: "sass-loader",
                            options: {
                                api: "modern",
                                sassOptions: {
                                    // Your sass options
                                },
                            },
                        },
                    ],
                },
                {
                    test: /\.(png|jpe?g|gif)$/i,
                    use: [
                        {
                            loader: "file-loader",
                            options: {
                                name: "[path][name].[ext]",
                            },
                        },
                    ],
                },
            ],
        },
        resolve: {
            extensions: ["*", ".js", ".jsx"],
            alias: {
                "@components": path.resolve(
                    __dirname,
                    "src/components/",
                ),
                "@views": path.resolve(
                    __dirname,
                    "src/views/",
                ),
            },
        },
        output: {
            path: path.resolve(__dirname, "dist/"),
            publicPath: "/dist/",
            filename: "[name].js",
        },
        devtool: is_dev_build_mode ? "source-map" : false,
        devServer: {
            client: {
                webSocketURL: env.DEV_SERVER_WS_URL,
                overlay: {
                    runtimeErrors: (error) => {
                        const ignoreErrors = [
                            "ResizeObserver loop limit exceeded",
                            "ResizeObserver loop completed with undelivered notifications.",
                        ];
                        if (ignoreErrors.includes(error.message)) {
                            return false;
                        }
                        return true;
                    },
                },
            },
            static: {
                directory: path.join(__dirname, "public/"),
            },
            // port: env.DEV_SERVER_PORT,
            port: 3000,
            host: "0.0.0.0",
            liveReload: true,
            allowedHosts: "all",
            historyApiFallback: true, // redirect to index.js if error
        },
        plugins: [
            new webpack.DefinePlugin({
                "process.env.API_URL": JSON.stringify(process.env.API_URL || "http://127.0.0.1:9999"),
            }),
            ...(is_dev_build_mode ? [new webpack.HotModuleReplacementPlugin()] : []),
            new webpack.ProvidePlugin({
                React: "react",
            }),
        ],
        optimization: {
            minimize: is_dev_build_mode ? false : true,
         },
        watchOptions: {
            poll: true,
            ignored: "**/node_modules/",
        },
    };
};
