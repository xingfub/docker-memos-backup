<template>
  <div class="backup-tab">
    <div class="backup-selector">
      <button 
        v-for="type in backupTypes" 
        :key="type.value"
        :class="['backup-btn', { active: backupType === type.value }]"
        @click="backupType = type.value"
      >
        <span class="icon">{{ type.icon }}</span>
        <span class="label">{{ type.label }}</span>
      </button>
    </div>

    <div class="form-card">
      <div v-if="backupType === 'email'" class="form-content">
        <h4 class="form-title">📧 邮箱备份配置</h4>
        <div class="form-group">
          <label>收件邮箱</label>
          <input 
            v-model="emailConfig.to_email" 
            class="form-input" 
            placeholder="to@example.com"
          />
        </div>
      </div>

      <div v-else-if="backupType === 'webdav'" class="form-content">
        <h4 class="form-title">☁️ WebDAV备份配置</h4>
        <div class="form-group">
          <label>WebDAV地址</label>
          <input 
            v-model="webdavConfig.url" 
            class="form-input" 
            placeholder="https://dav.example.com"
          />
        </div>
        <div class="form-group">
          <label>用户名</label>
          <input 
            v-model="webdavConfig.username" 
            class="form-input" 
            placeholder="username"
          />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input 
            v-model="webdavConfig.password" 
            class="form-input" 
            placeholder="password"
          />
        </div>
      </div>

      <div v-else-if="backupType === 's3'" class="form-content">
        <h4 class="form-title">🗄️ S3备份配置</h4>
        <div class="form-group">
          <label>Endpoint URL</label>
          <input 
            v-model="s3Config.endpoint_url" 
            class="form-input" 
            placeholder="https://s3.example.com"
          />
        </div>
        <div class="form-group">
          <label>Access Key</label>
          <input 
            v-model="s3Config.access_key" 
            class="form-input" 
            placeholder="AKIAXXXXXXXX"
          />
        </div>
        <div class="form-group">
          <label>Secret Key</label>
          <input 
            v-model="s3Config.secret_key" 
            type="password" 
            class="form-input" 
            placeholder="secret"
          />
        </div>
        <div class="form-group">
          <label>Bucket</label>
          <input 
            v-model="s3Config.bucket" 
            class="form-input" 
            placeholder="mybucket"
          />
        </div>
      </div>

      <div v-if="message" :class="['message', { success: success, error: !success }]">
        {{ message }}
      </div>

      <div class="form-actions">
        <button class="btn btn-primary" @click="saveBackup">
          <span class="btn-icon">💾</span>
          保存配置
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BackupTab',
  data() {
    return {
      backupType: 'email',
      backupTypes: [
        { value: 'email', label: '邮箱', icon: '📧' },
        { value: 'webdav', label: 'WebDAV', icon: '☁️' },
        { value: 's3', label: 'S3', icon: '🗄️' }
      ],
      emailConfig: {
        to_email: ''
      },
      webdavConfig: {
        url: '',
        username: '',
        password: ''
      },
      s3Config: {
        endpoint_url: '',
        access_key: '',
        secret_key: '',
        bucket: ''
      },
      message: '',
      success: false
    }
  },
  mounted() {
    this.loadConfig()
  },
  methods: {
    async loadConfig() {
      try {
        const res = await axios.get('/api/backup/config')
        if (res.data.code === 200) {
          this.emailConfig = { ...this.emailConfig, ...res.data.email }
          this.webdavConfig = { ...this.webdavConfig, ...res.data.webdav }
          this.s3Config = { ...this.s3Config, ...res.data.s3 }
        }
      } catch (e) {
        console.error(e)
      }
    },
    async saveBackup() {
      let params = {}
      let required = []

      if (this.backupType === 'email') {
        required = ['to_email']
        params = this.emailConfig
      } else if (this.backupType === 'webdav') {
        required = ['url', 'username', 'password']
        params = this.webdavConfig
      } else if (this.backupType === 's3') {
        required = ['endpoint_url', 'access_key', 'secret_key', 'bucket']
        params = this.s3Config
      }

      for (const key of required) {
        if (!params[key]) {
          const labels = {
            to_email: '收件邮箱',
            url: 'WebDAV地址',
            endpoint_url: 'Endpoint URL',
            access_key: 'Access Key',
            secret_key: 'Secret Key',
            bucket: 'Bucket'
          }
          return this.showMessage(`${labels[key]}不能为空`, false)
        }
      }

      try {
        const res = await axios.post('/api/backup', { type: this.backupType, params })
        this.showMessage(res.data.message, res.data.code === 200)
      } catch (e) {
        this.showMessage('保存失败', false)
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
.backup-tab {
  padding: 20px;
}

.backup-selector {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.backup-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
}

.backup-btn:hover {
  border-color: #d1d5db;
  transform: translateY(-2px);
}

.backup-btn.active {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}

.backup-btn .icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.backup-btn .label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.backup-btn.active .label {
  color: #667eea;
}

.form-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.form-title {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 6px;
}

.form-input {
  width: 100%;
  padding: 10px 14px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #9ca3af;
}

.message {
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 16px;
}

.message.success {
  background: #dcfce7;
  color: #166534;
}

.message.error {
  background: #fee2e2;
  color: #991b1b;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 16px;
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

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-icon {
  font-size: 16px;
}
</style>