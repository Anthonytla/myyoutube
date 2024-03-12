<template>
  <v-container>
    <h3>Username: {{ $auth.user.username }}</h3>
    <h3>Pseudo: {{ $auth.user.pseudo }}</h3>
    <h3>Email: {{ $auth.user.email }}</h3>
    <h3>Password: {{ $auth.user.password }}</h3>
    <v-btn to="/modify_user">Update</v-btn>
  </v-container>
</template>

<script>
export default {
  //ssr: false,
  //middleware: ['authenticated'],
  }
</script>


<style lang="scss" scoped>

</style>