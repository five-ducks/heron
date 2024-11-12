import { Component } from '../../core/core.js'

export class CustomAlert extends Component {
  constructor(payload = {}) {
    super({
      tagName: 'div',
      props: { 
        className: 'custom-alert-overlay',
        role: 'dialog',
        'aria-modal': 'true',
        'aria-labelledby': 'alert-message'
      },
      ...payload
    })
    this.message = payload.message || ''
    this.okButtonText = payload.okButtonText || '확인'
    this.resolvePromise = null
  }

  render() {
    this.el.innerHTML = ''
    
    const alertBox = document.createElement('div')
    alertBox.className = 'custom-alert-box'

    const messageText = document.createElement('p')
    messageText.id = 'alert-message'
    messageText.className = 'custom-alert-message'
    messageText.textContent = this.message
    alertBox.appendChild(messageText)

    const okButton = document.createElement('button')
    okButton.className = 'custom-alert-button'
    okButton.textContent = this.okButtonText
    okButton.onclick = () => this.close()
    alertBox.appendChild(okButton)

    this.el.appendChild(alertBox)

    // Focus trap
    this.el.addEventListener('keydown', this.handleKeyDown.bind(this))
  }

  handleKeyDown(event) {
    if (event.key === 'Escape') {
      this.close()
    }
  }

  close() {
    document.body.removeChild(this.el)
    if (this.resolvePromise) {
      this.resolvePromise()
    }
  }

  show() {
    return new Promise((resolve) => {
      this.resolvePromise = resolve
      document.body.appendChild(this.el)
      const okButton = this.el.querySelector('.custom-alert-button')
      okButton.focus()
    })
  }
}