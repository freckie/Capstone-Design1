<template>
  <div class="content">
    <div class="content-wrapper" :key="$route.fullPath">

      <div v-if="!workspaceLoaded" style="color: red">Workspace not loaded!</div>

      <div v-else :key="image.now">
        <!-- Image Panel -->
        <div class="image-panel">
          <div class="image-wrapper" :key="image.filename">
            <span class="body-2">{{ image.filename }}</span>
            <v-img id="target-image" :src="image.filepath"></v-img>
          </div>
        </div>

        <v-divider></v-divider>

        <!-- Input Panel -->
        <div class="input-panel">
          <v-container>
            <v-row justify="space-around">
              <v-col
                v-for="digit in digits"
                :key="digit.id"
                :id="`input-digit-`+digit.id"
                cols="12"
                md="3"
              >
                <v-sheet
                  class="pa-12"
                  color="grey lighten-3"
                >
                  <v-sheet
                    :elevation="6"
                    class="mx-auto digit-wrapper"
                    height="80"
                    width="60"
                  >
                    <span class="display-3">{{ digit.value }}</span>
                  </v-sheet>
                </v-sheet>
              </v-col>
            </v-row>
          </v-container>
        </div>

        <!-- Control Panel -->
        <v-bottom-navigation class="control-panel">
          <v-btn value="prev" @click="prevImage">
            <span>Prev</span>
            <v-icon>mdi-skip-previous-outline</v-icon>
          </v-btn>

          <v-btn class="non-clickable">
            <span>{{ image.filename }}</span>
          </v-btn>

          <v-btn value="next" @click="nextImage">
            <span>Next</span>
            <v-icon>mdi-skip-next-outline</v-icon>
          </v-btn>
        </v-bottom-navigation>

        <v-snackbar
          v-model="snackbar.isOpened"
          :timeout="3000"
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
  </div>
</template>

<script>
export default {
  name: 'Main',
  data: () => ({
    workspaceLoaded: false,
    currDigitID: 0,
    digits: [
      { id: 0, value: '' },
      { id: 1, value: '' },
      { id: 2, value: '' },
      { id: 3, value: '' }
    ],
    image: {
      filepath: '',
      filename: '',
      now: null
    },
    snackbar: {
      isOpened: false,
      text: ''
    }
  }),
  mounted () {
    // Check if workspace loaded
    this.checkWorkspaceLoaded()

    // Detect current image data
    var vm = this
    const ipc = require('electron').ipcRenderer
    ipc.on('current-image-changed', function (event, curr) {
      console.log(curr)
      vm.image.now = curr.idx
      vm.image.filepath = curr.filepath
      vm.image.filename = curr.filename
      // vm.currDigitID = 0
      // vm.digits = curr.digits
      vm.loadDigits(curr.digits)
    })

    // Capture keydown events
    this._keyCapture()
  },
  methods: {
    checkWorkspaceLoaded () {
      const remote = require('electron').remote
      this.workspaceLoaded = remote.getGlobal('workspaceLoaded')
    },
    saveToCSV () {
      const ipc = require('electron').ipcRenderer
      // ipc.send('save-to-csv')
      var result = ipc.sendSync('save-to-csv')
      console.log(result)

      this.snackbar.text = result
      this.snackbar.isOpened = true
    },
    prevImage () {
      this._setCurrentImage('prev')
    },
    nextImage () {
      this._setCurrentImage('next')
    },
    inputDigit (keyCode) {
      if (this.currDigitID > 3) return false
      else {
        this.digits[this.currDigitID].value = keyCode - 48
        this.currDigitID++
        return true
      }
    },
    removeDigit () {
      if (this.currDigitID <= 0) return false
      else {
        this.digits[this.currDigitID - 1].value = ''
        this.currDigitID--
        return true
      }
    },
    loadDigits (newDigits) {
      var len = 0
      for (var i = 0; i < 4; i++) {
        if (newDigits[i].value !== '') len++
        else break
      }
      this.currDigitID = len
      this.digits = newDigits
      console.log(len)
    },
    _setCurrentImage (key) {
      const ipc = require('electron').ipcRenderer
      ipc.send('set-current', { key: key, digits: this.digits })
    },
    _clearDigits () {
      for (var i = 0; i < 4; i++) this.digits[i].value = ''
      this.currDigitID = 0
    },
    _keyCapture () {
      var vm = this
      window.addEventListener('keyup', function (e) {
        if (e.keyCode === 37) { // Left arrow
          vm.prevImage()
        } else if (e.keyCode === 39) { // Right arrow
          vm.nextImage()
        } else if (e.keyCode === 83) { // 's' Save
          vm.saveToCSV()
        } else if (e.keyCode >= 48 && e.keyCode <= 57) { // Numbers
          vm.inputDigit(e.keyCode)
        } else if (e.keyCode === 8 || e.keyCode === 46) { // Remove
          vm.removeDigit()
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/assets/scss/common.scss";

.image-panel {
  .image-wrapper {
    width: 240px;
    margin: 10px auto;

    #target-image {
      width: 240px;
      height: 240px;
      background-color: #000000;
    }
  }
}

.input-panel {
  .digit-wrapper {
    text-align: center;
    vertical-align: middle;
    display: table-cell;
  }
}

.control-panel {
  position: absolute;
  bottom: 0;
  padding-top: 5px;

  .non-clickable {
    cursor: default;
  }
}
</style>
