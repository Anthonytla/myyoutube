<template>
  <v-container>
    <user-auth-form
      buttonText="Modify"
      :submitForm="modifyUser"
      :hasEmail="true"
      :hasPseudo="true"
      :isPwd="true"
    ></user-auth-form>
  </v-container>
</template>

<script>
import UserAuthForm from "../components/UserAuthForm.vue";

export default {
  //middleware: ['authenticated'],
  components: { UserAuthForm },
  methods: {
    async modifyUser(userInfo) {
      try {
        var id = this.$auth.user.id;
        var res = await this.$axios.put(
          "/myapi/user/"+id.toString(),
          userInfo
          // {
          //   mode: "no-cors",
          //   method: "POST",
          //   headers: {'Access-Control-Allow-Origin': '*'}
          // }
        );

        this.$auth.setUser(res.data.data)
        this.$router.push("/profile");
        alert("hello" + this.$auth.user.username);
      } catch (e) {
        this.$router.push("/profile");
        alert(e);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
</style>