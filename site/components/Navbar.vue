<template>
  <nav class="navbar is-dark">
    <div class="container">
      <div class="navbar-brand">
        <nuxt-link class="navbar-item" to="/">myYoutube</nuxt-link>
        <button class="button navbar-burger">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
      <div class="field has-addons">
        <div class="control">
          <input v-model="input" class="input" type="text" placeholder="Find a video" @keyup.enter="search(input)">
        </div>
        <div class="control">
          <!-- <nuxt-link class="button is-info" :to="{name: 'results', params: { search_query:'input' } }">Search</nuxt-link> -->
          <a class="button is-info" @click="search(input)">
            Search
          </a>
        </div>
      </div>
      <div class="navbar-menu">
        <div class="navbar-end">
          <div
            class="navbar-item has-dropdown is-hoverable"
            v-if="isAuthenticated"
          >
            <a class="navbar-link">
              {{ loggedInUser.username }}
            </a>
            <div class="navbar-dropdown">
              <nuxt-link class="navbar-item" to="/upload"
                >Upload</nuxt-link
              >

              <nuxt-link class="navbar-item" to="/profile"
                >My Profile</nuxt-link
              >
              <hr class="navbar-divider" />
              <a class="navbar-item">Logout</a>
            </div>
          </div>
          <template v-else>
            <nuxt-link class="navbar-item" to="/register">Register</nuxt-link>
            <nuxt-link class="navbar-item" to="/login">Log In</nuxt-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      input: ''
    }
  },
  computed: {
    ...mapGetters(["isAuthenticated", "loggedInUser"]),
  },
  methods: {
    async search(input) {
      if (input != "") {
        this.$router.push({ path: '/results', query: {search_query: input} });
      }
    },
  }
};
</script>