package utils

import "time"

func Schedule(fct func(), delay time.Duration) chan bool {
    stop := make(chan bool)
    go func() {
        for {
            fct()
            select {
            case <-time.After(delay):
            case <-stop:
            log.Debug("Scheduler stopped...")
                return
            }
        }
    }()
    return stop
}