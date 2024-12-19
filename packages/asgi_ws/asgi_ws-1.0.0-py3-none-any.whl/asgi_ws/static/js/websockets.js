class WebSocketManager {
    constructor(url, getToken, messageCallback, minRetryTimeout = 500, maxRetryTimeout = 10000) {
        this.url = url;
        this.getToken = getToken;
        this.messageCallback = messageCallback;
        this.retryCount = 0;
        this.minRetryTimeout = minRetryTimeout;
        this.maxRetryTimeout = maxRetryTimeout;
    }

    async connect() {
        const token = await this.getToken();
        this.ws = new WebSocket(`${this.url}?token=${token}`);

        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.retryCount = 0;
        };

        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            const timeout = Math.min(this.minRetryTimeout * Math.pow(2, this.retryCount), this.maxRetryTimeout);
            setTimeout(() => {
                this.retryCount++;
                this.connect();
            }, timeout);
        };

        this.ws.onmessage = this.messageCallback;
    }
}
