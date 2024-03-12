<template>
  <v-form v-model="valid">
    <v-text-field
      v-model="userInfo.username"
      label="Name"
      :rules="[required('name')]"
    />

    <v-text-field v-model="userInfo.pseudo" label="Pseudo" v-if="hasPseudo" />

    <v-text-field
      v-model="userInfo.email"
      label="Email"
      v-if="hasEmail"
      :rules="[required('email'), emailFormat()]"
    />

    <v-text-field
      v-model="userInfo.password"
      label="Password"
      :type="showPassword ? 'text' : 'password'"
      :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
      @click:append="showPassword = !showPassword"
      counter="true"
      :rules="rules"
    />

    <v-btn @click="submitForm(userInfo)" :disabled="!valid">{{
      buttonText
    }}</v-btn>
  </v-form>
</template>

<script>
import validations from "@/utils/validations.js";
export default {
  data() {
    console.log(this.$auth.user);
    this.rules = [];
    if (this.isPwdRequired) {
      this.rules = [
        validations.required("password"),
        validations.minLength("password", 8),
      ];
    }
    return {
      valid: false,
      showPassword: false,
      userInfo: {
        username: this.$auth.user ? this.$auth.user.username : null,
        email: this.$auth.user ? this.$auth.user.email : null,
        password: this.$auth.user ? this.$auth.user.password : null,
        pseudo:
          this.$auth.user && this.$auth.user.pseudo
            ? this.$auth.user.pseudo
            : null,
      },
      ...validations,
    };
  },
  props: ["submitForm", "buttonText", "hasEmail", "hasPseudo", "isPwdRequired"],
};
</script>

<style lang="scss" scoped>
</style> 