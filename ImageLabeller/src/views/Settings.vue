<template>
  <div class="content">
    <div class="content-wrapper" :key="$route.fullPath">

      <!-- Output Control -->
      <v-expansion-panels
        class="control-panel"
        v-model="panels[0]"
      >
        <v-expansion-panel>
          <v-expansion-panel-header>Output File Control</v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-text-field
              v-model="output"
              label="Output Filename"
              prepend-icon="mdi-file-delimited-outline"
            >
              {{ output }}
            </v-text-field>
            <div class="control-button-wrapper">
              <v-btn class="control-button"
                small
                color="primary"
                @click="saveOutputFilename"
              >
                Save Filename
              </v-btn>
            </div>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>

      <v-divider></v-divider>

      <!-- Start Filename Control -->
      <v-expansion-panels
        class="start-filename-panel"
        v-model="panels[1]"
      >
        <v-expansion-panel>
          <v-expansion-panel-header>Start Filename Control</v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-text-field
              v-model="startFilename"
              label="Start Filename"
              prepend-icon="mdi-file-delimited-outline"
            >
              {{ startFilename }}
            </v-text-field>
            <div class="control-button-wrapper">
              <v-btn class="control-button"
                small
                color="primary"
                @click="saveStartFilename"
              >
                Save Filename
              </v-btn>
            </div>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>

      <v-divider></v-divider>

      <!-- Workspace Control -->
      <v-expansion-panels
        class="control-panel"
        v-model="panels[2]"
      >
        <v-expansion-panel>
          <v-expansion-panel-header>Workspace Control</v-expansion-panel-header>
          <v-expansion-panel-content>
            <span v-if='workspace !== null' class="font-italic font-weight-light">{{ workspace }}</span>
            <span v-else  class="font-italic font-weight-light">Please open your workspace</span>
            <div class="control-button-wrapper">
              <v-btn
                class="control-button"
                id="btn-workspace"
                small
                color="primary"
                @click="openWorkspace"
              >
                Open Workspace
              </v-btn>
            </div>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>

      <v-snackbar
        v-model="snackbar.isOpened"
        :timeout="4000"
      >
        {{ snackbar.text }}
        <v-btn
          color="blue"
          text
          @click="snackbar.isOpened = false"
        >
          Close
        </v-btn>
      </v-snackbar>

    </div>
  </div>
</template>

<script>
export default {
  name: 'settings',
  data: () => ({
    panels: [0, 0, 0],
    workspace: null,
    output: 'result.csv',
    startFilename: '0.png',
    snackbar: {
      isOpened: false,
      text: ''
    }
  }),
  mounted () {
    this.getSetting()
  },
  methods: {
    getSetting () {
      const remote = require('electron').remote

      var _workspace = remote.getGlobal('workspacePath')
      if (_workspace !== '') this.workspace = _workspace
      else this.workspace = null

      var _result = remote.getGlobal('resultFilename')
      if (_result !== '') this.output = _result
      else {
        this.output = 'result.csv'
        remote.getGlobal('setResultFilename')(this.output)
      }
    },
    openWorkspace () {
      var vm = this

      const ipc = require('electron').ipcRenderer

      ipc.send('open-file-dialog')
      ipc.on('selected-file', function (event, path) {
        vm.workspace = `${path}`
      })
      ipc.on('workspace-load-event', function (event, ok) {
        if (ok === true) {
          vm.snackbar.text = 'Workspace loaded successfully!'
          vm.snackbar.isOpened = true
        } else {
          vm.snackbar.text = 'Workspace loaded failed!'
          vm.snackbar.isOpened = true
        }
      })
    },
    saveOutputFilename () {
      const remote = require('electron').remote
      remote.getGlobal('setResultFilename')(this.output)
    },
    saveStartFilename () {
      const remote = require('electron').remote
      remote.getGlobal('setStartFilename')(this.startFilename)
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/common.scss";

.control-panel {
  margin: 10px 0;
}

.control-button-wrapper {
  float: right;
  .control-button {
    margin-right: 10px;
  }
}
</style>
