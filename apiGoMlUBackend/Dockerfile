# Stage 1: Build the Go application
FROM golang:1.22.6 AS builder

# Set the working directory inside the container
WORKDIR /appGo

# Copy go.mod and go.sum first to leverage Docker caching
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the rest of the code
COPY . ./

# Copy the .env file to the correct location inside the container
COPY  .env /appGo/.env

# Build the Go binary from the main.go in cmd/api
RUN CGO_ENABLED=0 GOOS=linux go build -o /appGo/go-execute ./cmd/main.go

# Stage 2: Run the application using a smaller base image
FROM alpine:latest

# Install any dependencies your binary might need, e.g., if it relies on SSL
RUN apk --no-cache add ca-certificates

WORKDIR /appGo

# Copy the .env file from the builder stage to the container
COPY --from=builder /appGo/.env /appGo/.env

# Copy the built binary from the builder stage
COPY --from=builder /appGo/go-execute /appGo/go-execute

# Expose port 8000 (or any port your app uses)
EXPOSE 8000

# Run the Go binary
CMD ["/appGo/go-execute"]
