<template>
  <n-config-provider :theme="darkTheme">
    <div class="frame">
      <div class="frame-title"><Icon style="margin-right: 8px;"><AdjustmentsAlt /></Icon> 串口控制面板</div>
      <div class="frame-content">
        <n-form-item 
        label="消息框"
        feedback-style="display: none;"
        > 
          <n-input
          v-model:value="terminalData"
          type="textarea"
          id="term"
          placeholder="终端"
          :autosize="{
            minRows: 10,
            maxRows: 10,
          }"
          :disabled="true"
          />
        </n-form-item> 
        <n-divider />
        <n-form-item 
        label="串口配置"
        :feedback="bConnected ? '已连接' : '尚未连接'"
        style="margin-bottom: 10px;"
        > 
        <n-dropdown trigger="click" :options="comOptions" @select="handleSelect">
          <n-button style="width: 25%; margin-right: 10px;" @click="fetchAvailablePorts">{{ currentSelect }}</n-button>
        </n-dropdown>
        <n-input-group>
        <n-input-group-label>波特率</n-input-group-label>
        <n-input 
        v-model:value="bandrate" 
        type="text" 
        style="margin-right: 10px;" 
        />
        </n-input-group>
        <n-button v-if="!bConnected" style="width: 25%;" type="primary" @click="connectPort">
          <template #icon>
            <Icon><BrandOpenSource /></Icon>
          </template>
          连接串口
        </n-button>
        <n-button v-else style="width: 25%;" type="error" @click="disconnectPort">
          <template #icon>
            <Icon><CircleX /></Icon>
          </template>
          断开连接
        </n-button>
        </n-form-item> 
        <n-form-item 
        label="发送数据"
        > 
          <n-input-group>
            <n-input 
            v-model:value="messageData" 
            type="text" 
            placeholder="输入消息" 
            :disabled="!bConnected"
            />
            <n-button type="primary" :disabled="!bConnected" @click="sendMessage">发送</n-button>
          </n-input-group>
        </n-form-item> 
      </div>
    </div>
    <div class="background">
      <img class="background-img" :src="wallpaper" alt="">
    </div>
  </n-config-provider>
</template>

<script setup lang="ts">
import axios from 'axios'
import wallpaper from '@/assets/wallpaper.jpg'
import { AdjustmentsAlt, BrandOpenSource, CircleX } from '@vicons/tabler'
import { Icon } from '@vicons/utils'
import { ref } from 'vue'
import { 
  NConfigProvider, 
  NDropdown, 
  NFormItem, 
  NDivider, 
  NInput, 
  NInputGroup, 
  NInputGroupLabel,
  NButton, 
  darkTheme 
} from 'naive-ui'

const terminalData = ref(``)
const messageData = ref()
const bConnected = ref(false)
const bandrate = ref('9600')
const comOptions = ref([
  {
    label: '加载端口',
    key: '加载端口'
  }
])
const currentSelect = ref('选择端口')

function handleSelect(key: string) {
  currentSelect.value = key
}

let handleInterval : any

async function connectPort() {
  if (currentSelect.value == '选择端口') return
  axios.post('http://127.0.0.1:5000/connect_port', {
    com: currentSelect.value,
    bandrate: bandrate.value
  }).then(() => {
    bConnected.value = true
    terminalData.value = ``
    if (handleInterval) {
      clearInterval(handleInterval)
    }
    handleInterval = setInterval(() => {
      readPort()
    }, 500)
  })
}

async function disconnectPort() {
  if (handleInterval) {
    clearInterval(handleInterval)
  }
  axios.get('http://127.0.0.1:5000/disconnect_port').then((e) => {
    bConnected.value = false
  })
}

async function fetchAvailablePorts() {
  axios.get('http://127.0.0.1:5000/get_ports').then((e) => {
    comOptions.value = []
    for (let i of e.data.ports) {
      comOptions.value.push({
        label: i,
        key: i
      })
    }
  })
}

async function readPort() {
  axios.get('http://127.0.0.1:5000/read').then((e) => {
    if(e.data.msg != '') {
      terminalData.value += e.data.msg
      let textarea = document.getElementsByClassName('n-input__textarea-el')[0]
      textarea.scrollTop = textarea.scrollHeight
    }
  })
}

async function sendMessage() {
  if(messageData.value == '') return
  axios.post('http://127.0.0.1:5000/write', {
    message: messageData.value
  }).then(() => {
    terminalData.value += '[SEND MESSAGE] ' + messageData.value + '\n'
    let textarea = document.getElementsByClassName('n-input__textarea-el')[0]
    textarea.scrollTop = textarea.scrollHeight
  })
}
</script>

<style scoped>
.frame {
  max-width: 1200px;
  height: 550px;
  width: 75vw;
  position: absolute;
  left: 50vw;
  top: 50vh;
  transform: translate(-50%, -50%);
  background-color: rgb(18, 18, 18);
  border-radius: 10px;
  overflow: hidden;
  z-index: 100;
}

.frame-title {
  width: 100%;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  font-weight: bolder;
  background-color: rgb(42, 42, 42);
}

.background {
  width: 100vw;
  height: 100vh;
  position: absolute;
  left: 0;
  top: 0;
  overflow: hidden;
  z-index: 10;
  background-color: rgb(0, 0, 0);
}

.connection {
  flex: 1;
}

.background-img {
  filter: blur(10px) saturate(40%);
}

.frame-content {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}

:deep(.n-input__textarea-el) {
  color: rgb(69, 196, 69) !important;
  cursor: text !important;
}
</style>
