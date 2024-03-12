export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'site',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: 'stylesheet',
        href: 'https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css'
      }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
  //  { src: '~/plugins/vue-sliding-pagination.js', mode: 'client' },
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    "@nuxtjs/vuetify"
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // https://go.nuxtjs.dev/pwa
    '@nuxtjs/pwa',
    // https://go.nuxtjs.dev/content
    '@nuxt/content',
    '@nuxtjs/auth',
    '@nuxtjs/proxy'
  ],

 
  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    //prefix: 'myapi/',
    //baseURL: "http://localhost:5000/myapi",
    headers: {
      "Content-type": "application/json",
    },
    proxy: true
  },
  proxy: {
      '/elasticsearch/': {
        target: 'http://es01:9200/',
         pathRewrite: {
           '^/elasticsearch': ''
         },
        changeOrigin: true
      },
      '/myapi/': {
        target: 'http://myapi:5000/',
        // pathRewrite: {
        //    '^/myapi/': ''
        //  },
        changeOrigin: true
      },
  },
  auth: {
      strategies: {
        local: {
          token: {
            required: true,
            type: 'Bearer',
            property: 'data.token'
          },
          user: {
            property: 'data',
            autoFetch: false
          },
          endpoints: {
            login: { url:'/myapi/auth', method:'post', propertyName: 'data.token' },
            logout: false,
            user: { url:'/myapi/auth/user', method: 'get', propertyName: 'data'}
          }
        }  
      }
    },

  // PWA module configuration: https://go.nuxtjs.dev/pwa
  pwa: {
    manifest: {
      lang: 'en'
    }
  },
  
  // Content module configuration: https://go.nuxtjs.dev/config-content
  content: {},

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  },
  server: {
    host: '0.0.0.0',
  },
}
