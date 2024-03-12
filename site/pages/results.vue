<template>
  <v-container v-if="isLoaded">
    <v-btn v-if="!$auth.loggedIn" to="/login">Login</v-btn>
    <v-btn v-if="!$auth.loggedIn" to="/register">Register</v-btn>
    <h3 v-if="$auth.loggedIn">Hello {{ $auth.user.username }}</h3>
    <v-btn v-if="$auth.loggedIn" class="navbar-item" @click="logout"
      >Logout</v-btn
    >
    <h1>Resultats de la recherche :</h1>
    <div v-if="videos.length == 0">
      <p>Nous n'avons pas trouvé de resultats pour cette recherche</p>
    </div>
    <div v-for="item in videos" :key="item._source.id">
      <!-- <select onChange="window.location.href=this.value">
        <option v-for="(uri, code) in item.formats" :value="'http://localhost:5000/'+`${uri}`" :key="code">
        {{code}}
        </option>
      </select> -->
      <nuxt-link :to="{path: '/watch', query: { v:item._source.id } }">
        <video class="thumbnail" preload="metadata">
          <source :src="'http://localhost:5000' + `${item._source.source}`+'#t=0.1'" type="video/mp4" />
        </video>
        <p>{{item._source.title}}</p>
      </nuxt-link>
    </div>
    <!-- <select>
      <option
        v-for="(uri, code) in item.formats"
        :value="'http://localhost:5000/' + `${uri}`"
        :key="code"
      >
        {{ code }}
      </option>
    </select> -->
    <!-- <div v-for="(uri, code) in item.formats" :key="code">
        <video controls width="250">
          <source :src="'http://localhost:5000/' + `${uri}`" type="video/mp4" />
        </video>
        <select onChange="window.location.href=this.value">
        <option disabled selected value> -- select a resolution -- </option>
        <option v-for="(uri, code) in item.formats" :value="'http://localhost:5000/'+`${uri}`" :key="code">
        {{code}}
        </option>
      </select>
      </div> -->

    <videos-pagination
      v-if="isLoaded"
      :currentPage="currentPage"
      :totalPages="totalPages"
      :onGoToSelect="pageChangeHandler"
    ></videos-pagination>
  </v-container>
</template>

<script>
import VideosPagination from "../components/VideosPagination.vue";
export default {
  components: { VideosPagination },
  data() {
    return {
      isLoaded: true,
      currentPage: this.currentPage,
      totalPages: this.totalPages,
      videos: this.videos ? this.videos : [],
      input: this.$route.query.search_query
    };
  },
  methods: {
    destroy() {
      this.$destroy();
    },
    pageChangeHandler(selectedPage) {
      this.currentPage = selectedPage;
      this.getVideos();
    },
    async logout() {
      await this.$auth.logout();
      //this.$auth.$storage.removeUniversal("user")
    },
    reload() {
      this.isLoaded = false;
      console.log("hello")
      this.$nextTick(() => {
        console.log("lala")
        this.isLoaded = true;
      });
    },
    async search(input) {
      /*if (!input) {
        return;
      }*/
      alert("You searched " + input);
      try {
        let query = {
          "query": {
            "multi_match": {
              "query": input, 
              "fields": [
                "title",
                "user.username^2"
              ],
              "fuzziness": "AUTO",
              "minimum_should_match": "70%"
            }
          }
        };
        let res = {};
        res = await this.$axios.post("elasticsearch/my_youtube_videos/_search", query);
        console.log(res);
        this.videos = res.data.hits.hits;
        //this.reload();
      } catch (e) {
        alert(e);
        console.log(e);
        this.error = e;
      }
    },
  },
  beforeMount() {
    this.search(this.input);
  },
};

</script>

<style scoped>
  .thumbnail {
    height: 200px;
  }

</style>
