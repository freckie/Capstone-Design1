'use strict'

import { app, protocol, BrowserWindow } from 'electron'
import {
  createProtocol
  /* installVueDevtools */
} from 'vue-cli-plugin-electron-builder/lib'
const isDevelopment = process.env.NODE_ENV !== 'production'

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let win

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([{ scheme: 'app', privileges: { secure: true, standard: true } }])

function createWindow () {
  // Create the browser window.
  win = new BrowserWindow({
    width: 1000,
    height: 600,
    titleBarStyle: 'customButtonsOnHover',
    webPreferences: {
      nodeIntegration: true,
      webSecurity: false
    }
  })
  win.removeMenu() // Remove top toolbar

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    win.loadURL('app://./index.html')
  }

  win.on('closed', () => {
    win = null
  })
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (win === null) {
    createWindow()
  }
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    // Devtools extensions are broken in Electron 6.0.0 and greater
    // See https://github.com/nklayman/vue-cli-plugin-electron-builder/issues/378 for more info
    // Electron will not launch with Devtools extensions installed on Windows 10 with dark mode
    // If you are not using Windows 10 dark mode, you may uncomment these lines
    // In addition, if the linked issue is closed, you can upgrade electron and uncomment these lines
    // try {
    //   await installVueDevtools()
    // } catch (e) {
    //   console.error('Vue Devtools failed to install:', e.toString())
    // }

  }
  createWindow()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', data => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}

/************************************/
/*              Custom              */
/************************************/
var fs = require('fs')
const ipc = require('electron').ipcMain

// global variables
global.workspacePath = ''
global.resultFilename = ''
global.startFilename = ''
global.workspaceLoaded = false
global.setResultFilename = function (val) {
  global.resultFilename = val
}
global.setStartFilename = function (val) {
  global.startFilename = val
}

// Variables
var wsControl = {
  filenames: [],
  fileLength: 0,
  current: {
    filename: '',
    filepath: '',
    idx: -1,
    digits: []
  }
}
var resultDigits = []

// functions
function loadWorkspace () {
  var files = fs.readdirSync(global.workspacePath)
  files.sort((a, b) => { return Number(a.substr(0, a.length - 3)) - Number(b.substr(0, b.length - 3)) })
  console.log(files)

  var nowStart = (global.startFilename === '')
  for (var i = 0; i < files.length; i++) {
    var _file = files[i]
    if (!nowStart) {
      if (_file === global.startFilename) nowStart = true
      else continue
    }

    var _suffix = _file.substr(_file.length - 4, _file.length)
    if (_suffix === '.png' || _suffix === '.PNG') {
      wsControl.filenames.push(_file)
      wsControl.fileLength = wsControl.filenames.length
    }
  }

  if (wsControl.fileLength === 0) {
    return false
  }
  return true
}

function setCurrentIdx (idx) {
  if (idx >= wsControl.fileLength || idx < 0) {
    return false
  }
  wsControl.current.idx = idx
  wsControl.current.filename = wsControl.filenames[idx]
  wsControl.current.filepath = global.workspacePath + '\\' + wsControl.filenames[idx]
  return true
}

function setCurrDigits (digits) {
  wsControl.current.digits = digits
  if (wsControl.current.idx < resultDigits.length) {
    resultDigits[wsControl.current.idx] = digits
  } else if (wsControl.current.idx >= resultDigits.length) {
    resultDigits.push(digits)
  }
}

function loadCurrDigits (idx) {
  if (idx < 0 || idx >= resultDigits.length) wsControl.current.digits = [{ id: 0, value: '' }, { id: 1, value: '' }, { id: 2, value: '' }, { id: 3, value: '' }]
  else wsControl.current.digits = resultDigits[idx]
}

function _digitsToLabels (digits) {
  var result = []
  var len = 0
  if (digits[0].value === '') return [0, 0, 10, 10, 10, 10]
  else {
    result.push(1) // hasNum
    result.push(0) // digitLen
    for (var i = 0; i < 4; i++) {
      if (digits[i].value !== '') {
        result.push(digits[i].value)
        len++
      } else {
        result.push(10)
      }
    }
    result[1] = len
  }
  return result
}

// Linked with openWorkspace() in "@/views/Settings"
// listen to an open-file-dialog command and sending back selected information
const dialog = require('electron').dialog

ipc.on('open-file-dialog', function (event) {
  dialog.showOpenDialog({
    properties: ['openDirectory']
  }, function (files) {
    if (files) {
      global.workspacePath = files[0]
      global.workspaceLoaded = loadWorkspace()
      event.sender.send('selected-file', files[0])
      event.sender.send('workspace-load-event', global.workspaceLoaded)
    }
  })
})

// Image control
ipc.on('set-current', function (event, data) {
  var ok = false

  if (data.key === 'prev') {
    setCurrDigits(data.digits)
    ok = setCurrentIdx(wsControl.current.idx - 1)
    loadCurrDigits(wsControl.current.idx)
  } else if (data.key === 'next') {
    setCurrDigits(data.digits)
    ok = setCurrentIdx(wsControl.current.idx + 1)
    loadCurrDigits(wsControl.current.idx)
  }

  if (ok) {
    event.sender.send('current-image-changed', wsControl.current)
  }
})

// Export as CSV
const createCsvWriter = require('csv-writer').createObjectCsvWriter
ipc.on('save-to-csv', function (event) {
  const csvWriter = createCsvWriter({
    path: global.workspacePath + '\\' + global.resultFilename,
    header: [
      { id: 'filename', title: 'FILENAME' },
      { id: 'label1', title: 'hasNum' },
      { id: 'label2', title: 'digitLen' },
      { id: 'label3', title: 'DIGIT1' },
      { id: 'label4', title: 'DIGIT2' },
      { id: 'label5', title: 'DIGIT3' },
      { id: 'label6', title: 'DIGIT4' }
    ]
  })

  var records = []
  for (var i = 0; i < resultDigits.length; i++) {
    var record = { filename: '', label1: 0, label2: 0, label3: 0, label4: 0, label5: 0, label6: 0 }
    var labels = _digitsToLabels(resultDigits[i])
    console.log(labels)
    record.filename = wsControl.filenames[i]
    record.label1 = labels[0]
    record.label2 = labels[1]
    record.label3 = labels[2]
    record.label4 = labels[3]
    record.label5 = labels[4]
    record.label6 = labels[5]
    records.push(record)
  }

  csvWriter.writeRecords(records)
    .then(() => {
      event.returnValue = 'Saved successfully.'
    })
    .catch(function (err) {
      event.returnValue = String(err)
    })
})
