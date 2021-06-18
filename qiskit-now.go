package main

import (
	"context"
	"fmt"
	"os"
	"os/user"

	"github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/api/types/mount"
	"github.com/docker/docker/client"
	"github.com/docker/docker/pkg/stdcopy"
	"github.com/docker/go-connections/nat"
)

func main() {
	ctx := context.Background()
	cli, err := client.NewClientWithOpts(client.FromEnv, client.WithAPIVersionNegotiation())
	if err != nil {
		panic(err)
	}

	userAndGroup, err := GetUserAndGroup()
	if err != nil {
		panic(err)
	}

	volumes := []mount.Mount{
		{
			Type:     mount.TypeBind,
			Source:   "/etc/group",
			Target:   "/etc/group",
			ReadOnly: true,
		},
		{
			Type:     mount.TypeBind,
			Source:   "/etc/passwd",
			Target:   "/etc/passwd",
			ReadOnly: true,
		},
		{
			Type:     mount.TypeBind,
			Source:   "/etc/shadow",
			Target:   "/etc/shadow",
			ReadOnly: true,
		},
		{
			Type:   mount.TypeBind,
			Source: os.Getenv("HOME"),
			Target: "/home",
		},
	}

	resp, err := cli.ContainerCreate(ctx, &container.Config{
		Tty:  true,
		User: userAndGroup,
		Env:  []string{"HOME=/home"},
		ExposedPorts: nat.PortSet{
			"8888/tcp": struct{}{},
		},
		WorkingDir: "/home",
		Image:      "delapuente/qiskitnow",
	}, &container.HostConfig{
		PortBindings: nat.PortMap{
			"8888/tcp": []nat.PortBinding{
				{
					HostIP:   "0.0.0.0",
					HostPort: "8888",
				},
			},
		},
		Mounts: volumes,
	}, nil, nil, "qiskit-now")
	if err != nil {
		panic(err)
	}

	if err := cli.ContainerStart(ctx, resp.ID, types.ContainerStartOptions{}); err != nil {
		panic(err)
	}

	statusCh, errCh := cli.ContainerWait(ctx, resp.ID, container.WaitConditionNotRunning)
	select {
	case err := <-errCh:
		if err != nil {
			panic(err)
		}
	case <-statusCh:
	}

	out, err := cli.ContainerLogs(ctx, resp.ID, types.ContainerLogsOptions{ShowStdout: true})
	if err != nil {
		panic(err)
	}

	stdcopy.StdCopy(os.Stdout, os.Stderr, out)
}

func GetUserAndGroup() (string, error) {
	currentUser, err := user.Current()
	if err != nil {
		return "", err
	}
	result := fmt.Sprintf("%s:%s", currentUser.Uid, currentUser.Gid)
	return result, nil
}
