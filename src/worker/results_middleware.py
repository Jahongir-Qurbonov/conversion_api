from dramatiq.results import Results


class CustomResults(Results):
    def before_process_message(self, broker, message):
        store_results, result_ttl = self._lookup_options(broker, message)
        if store_results:
            self.backend.store_result(message, {"state": 0}, result_ttl)
        if not store_results and message.options.get("pipe_target") is None:
            self.logger.warning(
                "Actor '%s' returned a value that is not None, but you "
                "haven't set its `store_results' option to `True' so "
                "the value has been discarded." % message.actor_name
            )

    def after_process_message(self, broker, message, *, result=None, exception=None):
        store_results, result_ttl = self._lookup_options(broker, message)
        if store_results and exception is None:
            self.backend.store_result(
                message, {"state": 100, "result": result}, result_ttl
            )
        if (
            not store_results
            and result is not None
            and message.options.get("pipe_target") is None
        ):
            self.logger.warning(
                "Actor '%s' returned a value that is not None, but you "
                "haven't set its `store_results' option to `True' so "
                "the value has been discarded." % message.actor_name
            )

    def after_skip_message(self, broker, message):
        """If the message was skipped but not failed, then store None.
        Let after_nack handle the case where the message was skipped and failed.
        """
        store_results, result_ttl = self._lookup_options(broker, message)
        if store_results and not message.failed:
            self.backend.store_result(message, {"state": None}, result_ttl)

    def after_nack(self, broker, message):
        store_results, result_ttl = self._lookup_options(broker, message)
        if store_results and message.failed:
            exception = message._exception or Exception("unknown")
            self.backend.store_exception(
                message, {"state": -1, "exception": exception}, result_ttl
            )
