<template>
  <v-container>
    <v-btn v-if="!$auth.loggedIn" to="/login">Login</v-btn>
    <v-btn v-if="!$auth.loggedIn" to="/register">Register</v-btn>
    <h3 v-if="$auth.loggedIn">Hello {{ $auth.user.username }}</h3>
    <v-btn v-if="$auth.loggedIn" class="navbar-item" @click="logout"
      >Logout</v-btn
    >


    <div v-for="item in videos" :key="item.id">
      <select onChange="window.location.href=this.value">
        <option disabled selected value> -- select a resolution -- </option>
        <option v-for="(uri, code) in item.formats" :value="'http://localhost:5000/'+`${uri}`" :key="code">
        {{code}}
        </option>
      </select>
      <video preload="metadata">
        <source :src="'http://localhost:5000' + `${item.source}`" type="video/mp4" />
      </video>
      <p>{{item.name}}</p>
      <v-btn v-if="$auth.loggedIn && $auth.user.id == item.user.id" @click="remove(item)">Delete</v-btn>
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
      isLoaded: false,
      currentPage: this.currentPage,
      totalPages: this.totalPages,
      videos: this.videos ? this.videos : [],
    };
  },
  methods: {
    pageChangeHandler(selectedPage) {
      this.currentPage = selectedPage;
      this.getVideos();
    },
    async logout() {
      await this.$auth.logout();
      //this.$auth.$storage.removeUniversal("user")
    },
    async getVideos() {
      try {
        var that = this;
        console.log("currentpage", this.currentPage);
        return await this.$axios
          .get("/myapi/videos", {
            params: {
              page: this.currentPage,
            },
          })
          .then(function (result) {
            if (result.data.data.length == 0) {
              return;
            }
            that.videos = result.data.data;
            console.log("IN", that.videos);
            that.totalPages = result.data.pager.total;
            console.log("OUT", that.totalPages)
            return;
          })
          .then(function () {
            that.isLoaded = true;
          });
      } catch (e) {
        console.log(e.response);
        this.error = e.response.data;
      }
    },
    async remove(video) {
      var that = this;
        return await this.$axios
          .delete("/myapi/video/"+video.id)
          .then(function() {
            that.videos = that.getVideos();
          })
    }
  },
  beforeMount() {
    this.getVideos();
  },
};

</script>

<style scoped>

</style>
