"""Command-line flags."""

from absl import flags

FLAGS = flags.FLAGS

# Required flags.
flags.DEFINE_string("domain", None, "The name of a PDDL domain.")
flags.mark_flag_as_required("domain")
flags.DEFINE_string("approach", None, "The name of an approach.")
flags.mark_flag_as_required("approach")
