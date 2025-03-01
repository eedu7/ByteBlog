import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

import SocialAuthentication from "@/features/auth/SocialAuthentication";
import SignUpForm from "./SignUpForm";

const SignUpCard = () => {
    return (
        <Card className="mx-4 w-[400px] md:w-[400px] lg:w-[450px]">
            <CardHeader>
                <CardTitle>Join Our Community</CardTitle>
                <CardDescription>
                    Sign up today to get access to the latest blog posts, exclusive content, and
                    join discussion with like-minded readers&#33;
                </CardDescription>
            </CardHeader>
            <CardContent>
                <SignUpForm />
            </CardContent>
            <CardFooter>
                <SocialAuthentication />
            </CardFooter>
        </Card>
    );
};

export default SignUpCard;
