<template>
    <v-container>
        <user-auth-form buttonText="Login" :submitForm="logUser" :hasEmail="false"></user-auth-form>
    </v-container>
</template>

<script>
import UserAuthForm from '../components/UserAuthForm.vue'


export default {
  /*ssr: false,
  middleware: 'guest_user',*/
  components: { UserAuthForm },
  methods: {
      async logUser(userInfo) {
        try {
          let res_auth = await this.$auth.loginWith('local', {
            data: {
              login: userInfo.username,
              password: userInfo.password
            },
          })
          this.$auth.setUser(res_auth.data.data.user)
          //this.$auth.$storage.setUniversal("user", res_auth.data.data.user)

          this.$router.push('/')
          alert("hello" + this.$auth.user.username)
        } catch (e) {
          alert(e)
        }
      }
     
    }, 
    
  }
    
</script>


<style lang="scss" scoped>

</style>