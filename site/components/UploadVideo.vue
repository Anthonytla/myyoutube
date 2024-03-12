<template>
  <div class="container">
    <div>
      <h2>Single File</h2>
      <hr />
      <label
        >Name
        <input type="text" v-model="name" />
      </label>
      <label
        >File
        <input type="file" @change="handleFileUpload($event)" />
      </label>
      <br />
      <button v-on:click="submitFile()">Submit</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      file: "",
      name: "",
    };
  },

  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },

    submitFile() {
      let formData = new FormData();
      formData.append("name", this.name);
      formData.append("source", this.file);

      var id = this.$auth.user.id;
      console.log(formData.getAll("name"));
      this.$axios
        .post("/myapi/user/" + id.toString() + "/video", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then(function () {
          console.log("SUCCESS!!");
        })
        .catch(function (e) {
          console.log(e.response);
          console.log("FAILURE!!");
        });
    },
  },
};
</script>