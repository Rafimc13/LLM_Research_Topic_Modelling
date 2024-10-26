function formatDate(dateString) {
  // Create a Date object from the string
  const date = new Date(dateString)

  // Get the day, month, year, hours, and minutes
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0') // Months are 0-based
  const year = date.getFullYear()
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')

  // Format as dd/mm/yyyy hh:mm
  const formattedDate = `${day}/${month}/${year} ${hours}:${minutes}`

  return formattedDate
}

export { formatDate }
