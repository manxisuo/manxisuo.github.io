
function padNum(num, maxLength) {
    return num.toString().padStart(maxLength, '0')
}

function convertTime(githubTime) {
    const d = new Date(githubTime)
    const year = d.getFullYear()
    const month = padNum(d.getMonth() + 1, 2)
    const day = padNum(d.getDate(), 2)
    const hours = padNum(d.getHours(), 2)
    const minutes = padNum(d.getMinutes(), 2)
    const seconds = padNum(d.getSeconds(), 2)
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

export default {
    convertTime
}