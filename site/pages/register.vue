<template>
    <v-container>
        <user-auth-form buttonText="Register" :submitForm="registerUser" :hasEmail="true" :hasPseudo="false" isPwdRequired="true"></user-auth-form>
    </v-container>
</template>

<script>
import UserAuthForm from "../components/UserAuthForm.vue";
export default {
  //middleware: 'guest_user',
  components: { UserAuthForm },
  methods: {
    async registerUser(registerInfo) {
      try {
        await this.$axios.post(
          "/myapi/user",
          registerInfo,
          // {
          //   mode: "no-cors",
          //   method: "POST",
          //   headers: {'Access-Control-Allow-Origin': '*'}
          // }
        );
        let res_auth = await this.$auth.loginWith("local", {
          data: {
            login: registerInfo.username,
            password: registerInfo.password,
          },
        });
        console.log(res_auth.data.data.user);
        this.$auth.setUser(res_auth.data.data.user);
        console.log(this.$auth.user.id);
        console.log(res_auth.data.data.token);
        //await this.$auth.logout()
        if (this.$auth.loggedIn) {
          alert("logged in !");
        }
        this.$router.push("/");
        console.log(this.$auth.user.id);
        let token = this.$auth.getToken("local");
        console.log(token);
      } catch (e) {
        console.log(e.response.data);
        this.error = e.response.data;
      }
      //   this.$axios.get("http://localhost:5000/myapi/user/2")
      //   .then(function(results){
      //       console.log(results)
      //   })
    },
  },
};
</script>

<style lang="scss" scoped>
</style>