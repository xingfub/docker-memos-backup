<template>
  <div class="restore-tab">
    <div class="upload-card">
      <div class="upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
        <input 
          ref="fileInput" 
          type="file" 
          class="file-input" 
          @change="handleFileSelect"
          style="display: none;"
        />
        <div class="upload-icon">📁</div>
        <div class="upload-text">点击或拖拽文件到此处</div>
        <div class="upload-hint">支持任意文件格式</div>
      </div>

      <div v-if="selectedFile" class="file-info">
        <div class="file-icon">📄</div>
        <div class="file-details">
          <div class="file-name">{{ selectedFile.name }}</div>
          <div class="file-size">{{ formatSize(selectedFile.size) }}</div>
        </div>
        <button class="remove-btn" @click="clearFile">✕</button>
      </div>

      <div v-if="message" :class="['message', { success: success, error: !success }]">
        {{ message }}
      </div>

      <div class="upload-progress" v-if="uploading">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
        <div class="progress-text">{{ progress }}%</div>
      </div>

      <div class="form-actions">
        <button 
          class="btn btn-primary" 
          :disabled="!selectedFile || uploading"
          @click="uploadFile"
        >
          <span class="btn-icon">⬆️</span>
          上传还原
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RestoreTab',
  data() {
    return {
      selectedFile: null,
      message: '',
      success: false,
      uploading: false,
      progress: 0
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    handleFileSelect(e) {
      const file = e.target.files[0]
      if (file) {
        this.selectedFile = file
      }
    },
    handleDrop(e) {
      const file = e.dataTransfer.files[0]
      if (file) {
        this.selectedFile = file
      }
    },
    clearFile() {
      this.selectedFile = null
      this.$refs.fileInput.value = ''
    },
    formatSize(bytes) {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },
    async uploadFile() {
      if (!this.selectedFile) return

      this.uploading = true
      this.progress = 0
      this.message = ''

      const formData = new FormData()
      formData.append('file', this.selectedFile)

      try {
        const interval = setInterval(() => {
          if (this.progress < 90) {
            this.progress += Math.random() * 10
          }
        }, 200)

        const res = await axios.post('/api/restore', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })

        clearInterval(interval)
        this.progress = 100

        setTimeout(() => {
          this.showMessage(res.data.message, res.data.code === 200)
          this.uploading = false
          this.progress = 0
          this.clearFile()
        }, 500)
      } catch (e) {
        this.uploading = false
        this.progress = 0
        this.showMessage('上传失败', false)
      }
    },
    showMessage(msg, isSuccess) {
      this.message = msg
      this.success = isSuccess
      setTimeout(() => {
        this.message = ''
      }, 3000)
    }
  }
}
</script>

<style scoped>
.restore-tab {
  padding: 20px;
}

.upload-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.upload-area {
  border: 2px dashed #e5e7eb;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #fafafa;
}

.upload-area:hover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}

.upload-area.dragover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.upload-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.upload-text {
  font-size: 16px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

.upload-hint {
  font-size: 13px;
  color: #9ca3af;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
  margin-top: 20px;
}

.file-icon {
  font-size: 32px;
}

.file-details {
  flex: 1;
}

.file-name {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.file-size {
  font-size: 12px;
  color: #9ca3af;
}

.remove-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 50%;
  background: #fee2e2;
  color: #ef4444;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.remove-btn:hover {
  background: #fecaca;
  transform: scale(1.1);
}

.message {
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  margin-top: 16px;
}

.message.success {
  background: #dcfce7;
  color: #166534;
}

.message.error {
  background: #fee2e2;
  color: #991b1b;
}

.upload-progress {
  margin-top: 16px;
}

.progress-bar {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  font-size: 12px;
  color: #667eea;
  margin-top: 8px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid #f3f4f6;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-icon {
  font-size: 16px;
}
</style>