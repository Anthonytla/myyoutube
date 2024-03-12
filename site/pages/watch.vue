<template>
  <v-container v-if="isLoaded">
    <v-btn v-if="!$auth.loggedIn" to="/login">Login</v-btn>
    <v-btn v-if="!$auth.loggedIn" to="/register">Register</v-btn>
    <h3 v-if="$auth.loggedIn">Hello {{ $auth.user.username }}</h3>
    <v-btn v-if="$auth.loggedIn" class="navbar-item" @click="logout"
      >Logout</v-btn
    >
     <select onChange="window.location.href=this.value">
       <option disabled selected value> -- select a resolution -- </option>
      <option v-for="(uri, code) in video.formats" :value="'http://localhost:5000/'+`${uri}`" :key="code">
      {{code}}
      </option>
    </select>
      <video preload="metadata" width="500">
        <source :src="'http://localhost:5000'+`${video.source}`" type="video/mp4" />
      </video>
      <p>{{video.name}}</p>
      <!-- <v-btn v-if="$auth.loggedIn && $auth.user.id == video.user.id" @click="remove(video)">Delete</v-btn> -->
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
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      isLoaded: true,
      video: this.video ? this.video : {},
      vid_id: this.$route.query.v
    };
  },
  methods: {
    destroy() {
      this.$destroy();
    },
    async logout() {
      await this.$auth.logout();
      //this.$auth.$storage.removeUniversal("user")
    },
    async getVideo(id) {
      let res = await this.$axios.get("myapi/video/" + id);
      this.video = res.data.data.Video;
      console.log(this.video.source);
    },
    reload() {
      this.isLoaded = false;
      console.log("hello")
      this.$nextTick(() => {
    console.log("lala")
    this.isLoaded = true;
      });
    },
  },
  beforeMount() {
    this.getVideo(this.vid_id);
  },
  async remove(video) {
      var that = this;
        return await this.$axios
          .delete("/myapi/video/"+video.id)
          .then(function() {
            that.videos = that.getVideos();
          })
    }
}
</script>
<style scoped>
  .video-frame {
    height: 500px
  }
</style>