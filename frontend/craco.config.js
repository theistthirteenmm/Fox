module.exports = {
  webpack: {
    configure: (webpackConfig, { env, paths }) => {
      // Disable React Refresh in development
      if (env === 'development') {
        // Remove React Refresh webpack plugin
        webpackConfig.plugins = webpackConfig.plugins.filter(
          plugin => plugin.constructor.name !== 'ReactRefreshWebpackPlugin'
        );
        
        // Remove React Refresh babel plugin
        const babelLoader = webpackConfig.module.rules
          .find(rule => rule.oneOf)
          ?.oneOf?.find(rule => rule.loader && rule.loader.includes('babel-loader'));
        
        if (babelLoader && babelLoader.options && babelLoader.options.plugins) {
          babelLoader.options.plugins = babelLoader.options.plugins.filter(
            plugin => !plugin.includes('react-refresh')
          );
        }
      }
      
      return webpackConfig;
    },
  },
};